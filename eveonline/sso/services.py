import base64
import json
import secrets
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.http import HttpRequest
from django.utils import timezone

User = get_user_model()

AUTHORIZATION_URL = getattr(settings, "SSO_AUTHORIZATION_URL", "https://login.eveonline.com/v2/oauth/authorize/")
TOKEN_URL = getattr(settings, "SSO_TOKEN_URL", "https://login.eveonline.com/v2/oauth/token")


def get_authorization_url(request: HttpRequest) -> str:
    state = secrets.token_urlsafe(16)
    request.session["state"] = state
    request.session.modified = True
    params = {
        "client_id": settings.SSO_CLIENT_ID,
        "redirect_uri": settings.SSO_CALLBACK_URL,
        "response_type": "code",
        "scope": settings.SSO_SCOPES,
        "state": state,
    }
    query_string = urllib.parse.urlencode(params)
    return f"{AUTHORIZATION_URL}?{query_string}"


def validate_callback(request: HttpRequest) -> bool:
    if "code" not in request.GET:
        return False
    if "state" not in request.GET:
        return False
    if "state" not in request.session:
        return False
    if request.GET["state"] != request.session["state"]:
        return False
    return True


def request_oauth_token(request: HttpRequest) -> dict:
    params = {
        "grant_type": "authorization_code",
        "code": request.GET["code"],
    }
    access_token = _request_access_token(params)
    return _parse_access_token(access_token=access_token)


def refresh_oauth_token(refresh_token: str) -> dict:
    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    access_token = _request_access_token(params)
    return _parse_access_token(access_token=access_token)


def _request_access_token(payload: dict) -> dict:
    payload = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        data=payload,
        headers=_get_basic_authorization_header(),
        method="POST",
        url=TOKEN_URL,
    )
    response = urllib.request.urlopen(request)
    content_bytes = response.read()
    content_json = json.loads(content_bytes)
    return content_json


def _get_basic_authorization_header() -> dict:
    credentials = f"{settings.SSO_CLIENT_ID}:{settings.SSO_SECRET_KEY}".encode("utf-8")
    credentials_b64 = base64.urlsafe_b64encode(credentials).decode("utf-8")
    basic_authorization_string = f"Basic {credentials_b64}"
    return {
        "Authorization": basic_authorization_string,
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com",
    }


def _parse_access_token(access_token: dict) -> dict:
    header_str, payload_str, signature_str = access_token["access_token"].split(".")
    decoded_payload: str = base64.b64decode(f"{payload_str}==").decode("utf-8")
    payload = json.loads(decoded_payload)
    character, eve, character_id_str = payload["sub"].split(":")
    character_id = int(character_id_str)
    expiration = timezone.datetime.fromtimestamp(
        timestamp=payload["exp"],
        tz=timezone.timezone.utc,
    )
    return {
        "access_token": access_token["access_token"],
        "character_id": character_id,
        "character_name": payload["name"],
        "expiration": expiration,
        "refresh_token": access_token["refresh_token"],
    }
