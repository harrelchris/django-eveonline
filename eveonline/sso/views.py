from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import RedirectView

from eveonline.sso import services
from eveonline.sso.models import Token

User = get_user_model()


class AuthorizeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return services.get_authorization_url(request=self.request)


class CallbackView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def get(self, request, *args, **kwargs):
        if not services.validate_callback(request=request):
            messages.error(
                request=request,
                message="Authorization validation failed. Please try again.",
            )
            return redirect(reverse_lazy(settings.LOGIN_URL))
        oauth_token = services.request_oauth_token(request)
        token = Token(**oauth_token)
        Token.objects.filter(character_id=token.character_id).delete()
        user, created = User.objects.get_or_create(
            id=token.character_id,
            username=token.character_name,
        )
        token.save()
        user.token = token
        user.save()
        login(request, user)
        return super().get(request, *args, **kwargs)


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(settings.LOGOUT_REDIRECT_URL)

    def get(self, request, *args, **kwargs):
        Token.objects.filter(character_id=request.user.id).delete()
        logout(request=request)
        return super().get(request, *args, **kwargs)
