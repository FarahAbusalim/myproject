from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    #User management(register/, login/, change-password/)
    path('api/users/', include('user_management.urls')),  # ✅ استخدم فقط هذا

    #Advertisements
    path('api/ads/', include('advertisements.urls')),

    # Q&A section
    path('api/qa/', include('qa.urls')),
]
