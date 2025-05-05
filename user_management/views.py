# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from user_management.models import CustomUser
from .serializers import ChangePasswordSerializer

class RegisterView(APIView):
    def post(self, request):
        # عملية التسجيل
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        # عملية تسجيل الدخول
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # التوكنات يتم إرجاعها مباشرة من `LoginSerializer`
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # تأكد من أن المستخدم متوثق

    def put(self, request):
        # تغيير كلمة المرور
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(): # لو كانت الداتا صحيحة
            # تغيير كلمة المرور
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
