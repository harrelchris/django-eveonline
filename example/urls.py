from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sso/", include("sso.urls"), name="sso"),

    path("login/", TemplateView.as_view(template_name="login.html"), name="login"),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
]
