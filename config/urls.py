from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path

from finance.forms import BootstrapAuthenticationForm

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("finance.urls")),
    path(
        "accounts/login/",
        LoginView.as_view(authentication_form=BootstrapAuthenticationForm),
        name="login",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
]
