from rest_framework import serializers
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'  # يمكنك تحديد الحقول التي ترغب في إرجاعها هنا
