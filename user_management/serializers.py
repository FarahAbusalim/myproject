from rest_framework import serializers
from .models import CustomUser
import re
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# RegisterSerializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    student_id = serializers.CharField(max_length=10, min_length=10)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'gender', 'student_id']

    def validate_email(self, value):
        if not re.match(r'.+@ses\.yu\.edu\.jo$', value):
            raise serializers.ValidationError("Email must be a university email.")
        return value

    def validate_student_id(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Student ID must be exactly 10 digits.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[\W_]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

#LoginSerializer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

# ChangePasswordSerializer


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        user = self.context['request'].user  # الحصول على المستخدم المتوثق
        
        # التحقق من كلمة المرور الحالية
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError("Current password is incorrect")

        # التحقق من كلمة المرور الجديدة وفقًا للمتطلبات
        new_password = data['new_password']
        
        # تحقق من أن كلمة المرور الجديدة طولها على الأقل 8 أحرف
        if len(new_password) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        
        # تحقق من أن كلمة المرور تحتوي على حرف كبير
        if not re.search(r'[A-Z]', new_password):
            raise serializers.ValidationError("New password must contain at least one uppercase letter.")
        
        # تحقق من أن كلمة المرور تحتوي على رمز خاص
        if not re.search(r'[\W_]', new_password):  # \W يعني أي رمز غير حرف أو رقم
            raise serializers.ValidationError("New password must contain at least one special character.")
        
        return data
