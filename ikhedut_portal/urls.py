from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

admin.site.site_header = "ikhedut Portal Admin Panel"
admin.site.site_title = "ikhedut Portal"
admin.site.index_title = "Welcome to ikhedut Portal Admin"

urlpatterns = [    
    path('admin/', admin.site.urls),
    path("",include('ikhedut.urls')),
    
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)