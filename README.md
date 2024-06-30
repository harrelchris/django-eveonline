# Django Eve Online

Eve Online applications for Django

## Application

You must first create an application at https://developers.eveonline.com/

## Install

1. Install the library

    ```shell
    pip install django-eveonline
    ```

1. Add to `INSTALLED_APPS` in `settings.py`

    ```python
    INSTALLED_APP = [
        "sso.apps.SSOConfig",
    ]
    ```

1. Add to `urlpatterns` in `urls.py`

    ```python
    from django.urls import include, path
    
    urlpatterns = [
        path("sso/", include("sso.urls"), name="sso"),
    ]
    ```

1. Set environment variables.
    - Put these in a `.env` file and use [django-environ](https://django-environ.readthedocs.io/en/latest/index.html)

    ```python
    SSO_CLIENT_ID = env.str("SSO_CLIENT_ID")
    SSO_SECRET_KEY = env.str("SSO_SECRET_KEY")
    SSO_SCOPES = env.str("SSO_SCOPES")
    SSO_CALLBACK_URL = env.str("SSO_CALLBACK_URL")
    ```

1. Apply migrations

    ```shell
    python manage.py migrate
    ```
