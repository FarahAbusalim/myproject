from django.shortcuts import render
# qa/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.response import Response
from rest_framework.decorators import action

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:  # Students can manage their own questions
            permission_classes = [IsAuthenticated]
        else:  # Admin can manage everything
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def answer(self, request, pk=None):
        question = self.get_object()
        answer = Answer.objects.create(
            answer_text=request.data['answer_text'],
            user=request.user,
            question=question
        )
        serializer = AnswerSerializer(answer)
        return Response(serializer.data)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:  # Students can manage their own answers
            permission_classes = [IsAuthenticated]
        else:  # Admin can manage everything
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


