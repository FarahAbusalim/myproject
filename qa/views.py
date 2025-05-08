from django.shortcuts import render
# qa/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'answer']:
            # السماح لأي مستخدم مسجل بالدخول
            permission_classes = [IsAuthenticated]
        else:
            # مشاهدة الأسئلة مسموحة للجميع (يمكنك تعديلها حسب الحاجة)
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    #perform_update و perform_destroy: يسمح فقط لصاحب السؤال أو الأدمن.

    def perform_update(self, serializer):
        question = self.get_object()
        if self.request.user != question.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only edit your own question.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own question.")
        instance.delete()

    @action(detail=True, methods=['post'])
    def answer(self, request, pk=None):
        question = self.get_object()
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, question=question)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all().order_by('-created_at')
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        answer = self.get_object()
        if self.request.user != answer.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only edit your own answer.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own answer.")
        instance.delete()

