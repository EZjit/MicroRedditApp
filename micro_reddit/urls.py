from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home_page


urlpatterns = [
    path("", home_page, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('posts/', include('core.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('api/core/', include('core.api.urls')),
    path('api/users/', include('users.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
