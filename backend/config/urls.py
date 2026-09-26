from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.auth_urls")),
    path("api/users/", include("users.urls")),
    path("api/couples/", include("couples.urls")),
    path("api/wishes/", include("wishes.urls")),
    path("api/files/", include("files.urls")),
    path("api/lists/", include("lists.urls")),
    path("api/plans/", include("plans.urls")),
    path("api/menu/", include("menu.urls")),
]
