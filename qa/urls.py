# qa/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, AnswerViewSet


router = DefaultRouter()
router.register(r'questions', QuestionViewSet) #بيوفر الend points تلقائيا للسؤال 

urlpatterns = [
    path('', include(router.urls)),
]
