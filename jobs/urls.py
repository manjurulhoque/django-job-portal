from django.urls import re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.flatpages import views as flatpages_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView

from jobs.sitemaps import Sitemaps, StaticViewSitemap

schema_view = get_schema_view(
    openapi.Info(
        title="Jobs Portal API",
        default_version="v1",
        description="Jobs Portal Api Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

lang_patterns = i18n_patterns(path("", include("jobsapp.urls")), path("", include("accounts.urls")))

# sitemaps = {
#     '': JobViewSitemap
# }

urlpatterns = lang_patterns + [
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(
            [
                path("swagger", schema_view.with_ui("swagger", cache_timeout=0)),
                path("", include("accounts.api.urls")),
                path("", include("jobsapp.api.urls")),
                path("", include("tags.api.urls")),
                # path('auth/oauth/', include('rest_framework_social_oauth2.urls'))
            ]
        ),
    ),
    path("social-auth/", include("social_django.urls", namespace="social")),
    # url(r"^(?P<url>.*/)$", flatpages_views.flatpage),
    path("sitemap.xml/", sitemap, {"sitemaps": dict(Sitemaps())}, name="django.contrib.sitemaps.views.sitemap"),
    path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]
