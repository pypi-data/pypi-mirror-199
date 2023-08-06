import logging
from urllib.parse import quote

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView,
    logout_then_login as auth_logout_then_login)
from django.forms.forms import ErrorDict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from djblets.auth.views import register
from djblets.configforms.views import ConfigPagesView
from djblets.features.decorators import feature_required
from djblets.forms.fieldsets import filter_fieldsets
from djblets.siteconfig.models import SiteConfiguration
from djblets.util.decorators import augment_method_from
from djblets.views.generic.etag import ETagViewMixin

from reviewboard.accounts.backends import get_enabled_auth_backends
from reviewboard.accounts.forms.registration import RegistrationForm
from reviewboard.accounts.mixins import CheckLoginRequiredViewMixin
from reviewboard.accounts.pages import AccountPage, OAuth2Page, PrivacyPage
from reviewboard.accounts.privacy import is_consent_missing
from reviewboard.accounts.sso.backends import sso_backends
from reviewboard.admin.decorators import check_read_only
from reviewboard.avatars import avatar_services
from reviewboard.notifications.email.decorators import preview_email
from reviewboard.notifications.email.message import \
    prepare_password_changed_mail
from reviewboard.oauth.features import oauth2_service_feature
from reviewboard.oauth.forms import (UserApplicationChangeForm,
                                     UserApplicationCreationForm)
from reviewboard.oauth.models import Application
from reviewboard.site.mixins import CheckLocalSiteAccessViewMixin
from reviewboard.site.urlresolvers import local_site_reverse


logger = logging.getLogger(__name__)


class LoginView(DjangoLoginView):
    """A view for rendering the login page.

    Version Added:
        5.0
    """

    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        """Dispatch the view.

        Args:
            request (django.http.HttpRequest):
                The HTTP request.

            *args (tuple):
                Positional arguments to pass through to the parent class.

            **kwargs (dict):
                Keyword arguments to pass through to the parent class.

        Returns:
            django.http.HttpResponse:
            The response to send to the client.
        """
        siteconfig = SiteConfiguration.objects.get_current()
        sso_auto_login_backend = siteconfig.get('sso_auto_login_backend', None)

        if sso_auto_login_backend:
            try:
                backend = sso_backends.get('backend_id', sso_auto_login_backend)
                login_url = backend.login_url

                redirect_to = self.get_success_url()

                if is_safe_url(url=redirect_to, host=request.get_host()):
                    login_url = '%s?%s=%s' % (login_url,
                                              self.redirect_field_name,
                                              quote(redirect_to))

                return HttpResponseRedirect(login_url)
            except sso_backends.ItemLookupError:
                logging.error('Unable to find sso_auto_login_backend "%s".',
                              sso_auto_login_backend)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Return extra data for rendering the template.

        Args:
            **kwargs (dict):
                Keyword arguments to pass to the parent class.

        Returns:
            dict:
            Context to use when rendering the template.
        """
        context = super().get_context_data(**kwargs)

        context['enabled_sso_backends'] = [
            sso_backend
            for sso_backend in sso_backends
            if sso_backend.is_enabled()
        ]

        return context


def logout(request, *args, **kwargs):
    """Log out the user."""
    siteconfig = SiteConfiguration.objects.get_current()
    sso_auto_login_backend = siteconfig.get('sso_auto_login_backend', None)

    # If we're configured to automatically log in via SSO, we can't use
    # logout_then_login, because it will log out and then immediately log in
    # again.
    if sso_auto_login_backend:
        try:
            backend = sso_backends.get('backend_id', sso_auto_login_backend)
            return LogoutView.as_view()(request, *args, **kwargs)
        except sso_backends.ItemLookupError:
            logging.error('Unable to find sso_auto_login_backend "%s".',
                          sso_auto_login_backend)

    return auth_logout_then_login(request, *args, **kwargs)


class UserInfoboxView(CheckLoginRequiredViewMixin,
                      CheckLocalSiteAccessViewMixin,
                      ETagViewMixin,
                      TemplateView):
    """Displays information on a user, for use in user pop-up infoboxes.

    This is meant to be embedded in other pages, rather than being
    a standalone page.
    """

    template_name = 'accounts/user_infobox.html'

    def __init__(self, **kwargs):
        """Initialize a view for the request.

        Args:
            **kwargs (dict):
                Keyword arguments passed to :py:meth:`as_view`.
        """
        super(UserInfoboxView, self).__init__(**kwargs)

        self._lookup_user = None
        self._show_profile = None
        self._timezone = None

    def get_etag_data(self, request, username, *args, **kwargs):
        """Return an ETag for the view.

        This will look up some state needed for the request and generate a
        suitable ETag.

        Args:
            request (django.http.HttpRequest):
                The HTTP request from the client.

            username (unicode):
                The username of the user being looked up.

            *args (tuple):
                Positional arguments to pass to the handler.

            **kwargs (tuple):
                Keyword arguments to pass to the handler.

                These will be arguments provided by the URL pattern.

        Returns:
            unicode:
            The ETag for the page.
        """
        from reviewboard.extensions.hooks import UserInfoboxHook

        user = get_object_or_404(User, username=username)
        self._lookup_user = user

        profile = user.get_profile()
        self._show_profile = user.is_profile_visible(request.user)
        self._timezone = profile.timezone

        etag_data = [
            user.first_name,
            user.last_name,
            user.email,
            str(user.last_login),
            str(settings.TEMPLATE_SERIAL),
            str(self._show_profile),
            self._timezone,
        ]

        if avatar_services.avatars_enabled:
            avatar_service = avatar_services.for_user(user)

            if avatar_service:
                etag_data.extend(avatar_service.get_etag_data(user))

        local_site = self.local_site

        for hook in UserInfoboxHook.hooks:
            try:
                etag_data.append(hook.get_etag_data(
                    user=user,
                    request=request,
                    local_site=local_site))
            except Exception as e:
                logger.exception('Error when running UserInfoboxHook.'
                                 'get_etag_data method in extension "%s": %s',
                                 hook.extension.id, e)

        return ':'.join(etag_data)

    def get_context_data(self, **kwargs):
        """Return data for the template.

        This will return information on the user, along with information from
        any extension hooks used for the page.

        Args:
            **kwargs (tuple):
                Additional keyword arguments from the URL pattern.

        Returns:
            dict:
            Context data for the template.
        """
        from reviewboard.extensions.hooks import UserInfoboxHook

        # These are accessed several times, so bring them in to reduce
        # attribute lookups.
        user = self._lookup_user
        username = user.username
        local_site = self.local_site

        extra_content = []

        for hook in UserInfoboxHook.hooks:
            try:
                extra_content.append(hook.render(
                    user=user,
                    request=self.request,
                    local_site=local_site))
            except Exception as e:
                logger.exception('Error when running UserInfoboxHook.'
                                 'render method in extension "%s": %s',
                                 hook.extension.id, e)

        review_requests_url = local_site_reverse('user', local_site=local_site,
                                                 args=[username])
        reviews_url = local_site_reverse('user-grid', local_site=local_site,
                                         args=[username, 'reviews'])

        has_avatar = (
            avatar_services.avatars_enabled and
            avatar_services.for_user(user) is not None
        )

        return {
            'extra_content': mark_safe(''.join(extra_content)),
            'full_name': user.get_full_name(),
            'has_avatar': has_avatar,
            'infobox_user': user,
            'review_requests_url': review_requests_url,
            'reviews_url': reviews_url,
            'show_profile': self._show_profile,
            'timezone': self._timezone,
        }


@csrf_protect
def account_register(request, next_url='dashboard'):
    """Display the appropriate registration page.

    If registration is enabled and the selected authentication backend supports
    creation of users, this will return the appropriate registration page. If
    registration is not supported, this will redirect to the login view.
    """
    siteconfig = SiteConfiguration.objects.get_current()
    auth_backends = get_enabled_auth_backends()

    if (auth_backends[0].supports_registration and
        siteconfig.get('auth_enable_registration') and
        not siteconfig.get('site_read_only')):
        response = register(request, next_page=reverse(next_url),
                            form_class=RegistrationForm)

        return response

    return HttpResponseRedirect(reverse("login"))


class MyAccountView(ConfigPagesView):
    """Displays the My Account page containing user preferences.

    The page will be built based on registered pages and forms. This makes
    it easy to plug in new bits of UI for the page, which is handy for
    extensions that want to offer customization for users.
    """

    title = _('My Account')

    css_bundle_names = [
        'account-page',
    ]

    js_bundle_names = [
        '3rdparty-jsonlint',
        'config-forms',
        'account-page',
    ]

    @method_decorator(login_required)
    @method_decorator(check_read_only)
    @augment_method_from(ConfigPagesView)
    def dispatch(self, *args, **kwargs):
        """Handle the view.

        This just falls back to the djblets ConfigPagesView.dispatch
        implementation.
        """
        pass

    @property
    def nav_title(self):
        """Get the title for the navigation section."""
        return self.request.user.username

    @property
    def page_classes(self):
        """The list of page classes for this view.

        If the user is missing any consent requirements or has not accepted
        the privacy policy/terms of service, only the privacy page will be
        shown.
        """
        if self.is_user_missing_consent:
            return [AccountPage.registry.get('page_id', PrivacyPage.page_id)]

        return list(AccountPage.registry)

    @cached_property
    def ordered_user_local_sites(self):
        """Get the user's local sites, ordered by name."""
        return self.request.user.local_site.order_by('name')

    @property
    def render_sidebar(self):
        """Whether or not to render the sidebar.

        If the user is missing any consent requirements or has not accepted
        the privacy policy/terms of service, the sidebar will not render.
        This is to prevent the user from navigating away from the privacy page
        before making decisions.
        """
        return not self.is_user_missing_consent

    @cached_property
    def is_user_missing_consent(self):
        """Whether or not the user is missing consent."""
        return is_consent_missing(self.request.user)


@login_required
@preview_email(prepare_password_changed_mail)
def preview_password_changed_email(request):
    return {
        'user': request.user,
    }


@login_required
@feature_required(oauth2_service_feature)
def edit_oauth_app(request, app_id=None):
    """Create or edit an OAuth2 application.

    Args:
        request (django.http.HttpRequest):
            The current HTTP request.

        app_id (int, optional):
            The ID of the application to edit.

            If this argument is ``None`` a new application will be edited.

    Returns:
        django.http.HttpResponse:
        The rendered view.
    """
    # If we import this at global scope, it will cause issues with admin sites
    # being automatically registered.
    from reviewboard.oauth.admin import ApplicationAdmin

    if app_id:
        app = get_object_or_404(
            Application,
            pk=app_id,
            user=request.user,
        )
        form_cls = UserApplicationChangeForm
        fieldsets = ApplicationAdmin.fieldsets
    else:
        app = None
        form_cls = UserApplicationCreationForm
        fieldsets = ApplicationAdmin.add_fieldsets

    if request.method == 'POST':
        form_data = request.POST.copy()

        form = form_cls(user=request.user, data=form_data, initial=None,
                        instance=app)

        if form.is_valid():
            app = form.save()

            if app_id is not None:
                next_url = OAuth2Page.get_absolute_url()
            else:
                next_url = reverse('edit-oauth-app', args=(app.pk,))

            return HttpResponseRedirect(next_url)
    else:
        form = form_cls(user=request.user, data=None, initial=None,
                        instance=app)

        # Show a warning at the top of the form when the form is disabled for
        # security.
        #
        # We don't need to worry about full_clean not being called (which would
        # be if we went through form.errors) because this form will never be
        # saved.
        if app and app.is_disabled_for_security:
            form._errors = ErrorDict({
                '__all__': form.error_class(
                    [form.DISABLED_FOR_SECURITY_ERROR],
                ),
            })

    return render(
        request=request,
        template_name='accounts/edit_oauth_app.html',
        context={
            'app': app,
            'form': form,
            'fieldsets': filter_fieldsets(form=form_cls,
                                          fieldsets=fieldsets),
            'oauth2_page_url': OAuth2Page.get_absolute_url(),
            'request': request,
        })
