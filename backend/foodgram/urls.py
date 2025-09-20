from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from recipes.urls import router as recipes_router
from users.urls import router as users_router

api_patterns = users_router.urls + recipes_router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
    path('api/auth/', include('djoser.urls.authtoken')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
