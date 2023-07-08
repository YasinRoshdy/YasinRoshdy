"""mwasa2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.views.generic import TemplateView

from django.apps import AppConfig, apps
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sites.models import Site
from django.shortcuts import redirect
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from rest_framework import permissions
from rest_framework import authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# apps.app_configs["cms"].verbose_name = _("Al Mouassa")
apps.app_configs["filer"].verbose_name = _("Files and Directory's")
apps.app_configs["base"].verbose_name = _("BASE")

admin.site.site_url = "/"
Site.name = "Al Mouassa"
Site.domain = "http://127.0.0.1:8000/"

# settingsadmin.admin.sites.site.site_header = _("Al Mouassa")
# settingsadmin.admin.sites.site.name = _("Al Mouassa")
# settingsadmin.admin.sites.site.site_title = _("Al Mouassa")
# settingsadmin.admin.sites.site.site_url = _("http://127.0.0.1:8000/")

admin.autodiscover()
# default: "Django Administration"
admin.site.site_header = _("Al Mouassa")
# default: "Site administration"
admin.site.index_title = _("Features area")
# default: "Django site admin"
admin.site.site_title = _("Al Mouassa Site Admin")
# add user
from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib.auth.admin import UserAdmin

# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


apps.app_configs["admin"].verbose_name = _("admin")


# end  user

ADMIN_ORDERING = [
    (
        "base",
        [
            "General_information",
            "DailyPublish",
            "RelatedSites",
            "RelatedSites",
            "AyatTafsirVideo",
            "AyatTafsirAudio",
            "AyatTelawa",
            "TafsirHadithInAlSaheh",
            "OtherScience",
            "OtherScienceAudio",
            "OtherScienceSubject",
            "Book",
            "BookSeach",
            "Fatwa",
            "Sessions",
            "SessionsCategory",
            "CallUs",
            "PhoneNumbers",
            "Email",
            # temp
            "Hadith",
            "ChapterInAlSaheh",
            "BookInAlSaheh",
            "Ayat"
            # users
        ],
    ),
    ("auth", ["User", "Group", "Log"]),
]


def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in ADMIN_ORDERING:
        app = app_dict[app_name]
        app["models"].sort(key=lambda x: object_list.index(x["object_name"]))
        yield app


admin.AdminSite.get_app_list = get_app_list


# apps.app_configs["cms"].verbose_name = _("Al Mouassa")
apps.app_configs["filer"].verbose_name = _("Files and Directory's")
apps.app_configs["base"].verbose_name = _("BASE")
admin.site.site_url = "/"
Site.name = "Al Mouassa"
# from django.contrib.sites.models import Site
# site = Site.objects.create(domain="http://127.0.0.1:8000/", name="Al Mouassa")
# site.save()

# from rest_framework_swagger.views import get_swagger_view
# from django.conf.urls import url

# schema_view = get_swagger_view(title="Pastebin API")


schema_view = get_schema_view(
    openapi.Info(
        title="Al Mouassa API",
        default_version="v2",
        description="Al Mouassa Site API",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ms@nilelive.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[authentication.SessionAuthentication],
)
urlpatterns = [
    # re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # re_path(r"^swagger/$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    re_path("api.json", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    #     url(r"^$", schema_view),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("icons/shaikh.svg")),
    ),
    path("admin/", admin.site.urls),
    # path("dynamic-admin-form/", include("dynamic_admin_forms.urls")),
    # path("ckeditor/", include("ckeditor_uploader.urls")),
    path("dynamic-select/", include("dynamic_select.urls")),
    path("", include("base.urls"), name="base"),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
