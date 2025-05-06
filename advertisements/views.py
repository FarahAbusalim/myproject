from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Advertisement
from .serializers import AdvertisementSerializer

# ViewSet للإعلانات
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()  # جلب جميع الإعلانات
    serializer_class = AdvertisementSerializer  # الـ Serializer للإعلانات
    # ✅ دعم الترتيب حسب created_at
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # ← الترتيب الافتراضي: الأحدث أولًا

    # تحديد الصلاحيات
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:  # السماح بالقراءة فقط للمستخدمين العاديين
            permission_classes = [AllowAny]  # أي مستخدم (مسجل أو غير مسجل) يمكنه قراءة الإعلانات
        else:  # السماح فقط للأدمن بإضافة أو تعديل أو حذف الإعلانات
            permission_classes = [IsAuthenticated & IsAdminUser]
        return [permission() for permission in permission_classes]
