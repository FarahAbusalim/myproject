from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdvertisementViewSet

# إعداد الـ Router
router = DefaultRouter()
router.register(r'advertisements', AdvertisementViewSet)

# ربط الـ URL بإعدادات الـ ViewSet
urlpatterns = [
    path('', include(router.urls)),
]
