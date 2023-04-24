from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from E_Shop import settings
from electronics.views import ElectronicaViewSet, UserViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('api/users/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('api/electronics/', ElectronicaViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/electronics/<int:pk>/',
         ElectronicaViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    path('api/auth/', include('rest_framework.urls')),
    path('', include('electronics.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
