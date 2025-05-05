from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Advertisement
from .serializers import AdvertisementSerializer

# ViewSet للإعلانات
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()  # جلب جميع الإعلانات
    serializer_class = AdvertisementSerializer  # الـ Serializer للإعلانات

    # تحديد الصلاحيات
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # السماح بالقراءة فقط للمستخدمين العاديين
            permission_classes = [AllowAny]  # أي مستخدم (مسجل أو غير مسجل) يمكنه قراءة الإعلانات
        else:  # السماح فقط للأدمن بإضافة أو تعديل أو حذف الإعلانات
            permission_classes = [IsAuthenticated & IsAdminUser]
        return [permission() for permission in permission_classes]
