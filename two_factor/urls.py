"""two_factor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from core.views import (
    TOTPVerifyView,
    TOTPCreateView,
    CustomTokenObtainPairView,
    StaticCreateView,
    StaticVerifyView,
    TOTPDeleteView,
    login_view,
    update_user_ip,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^totp/create/$", TOTPCreateView.as_view(), name="totp-create"),
    re_path(
        r"^totp/login/(?P<token>[0-9]{6})/$",
        TOTPVerifyView.as_view(),
        name="totp-login",
    ),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("emergency/create/", StaticCreateView.as_view(), name="static-create"),
    re_path(
        r"^emergency/login/(?P<token>[a-z2-9]{7,8})/$",
        StaticVerifyView.as_view(),
        name="static-login",
    ),
    re_path(r"^totp/delete/$", TOTPDeleteView.as_view(), name="totp-delete"),
    path("login/", login_view, name="login"),
    path("ip/update/", update_user_ip, name="update_user_ip"),
]
