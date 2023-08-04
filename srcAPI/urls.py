from django.contrib import admin
from django.urls import path, include
from appAPI import urls
from rest_framework_simplejwt.views import  TokenRefreshView
from appAPI.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
    # path('auth/',include('djoser.urls')),
    # path('auth/',include('djoser.urls.authtoken')),

    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
