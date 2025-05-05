# qa/models.py
from django.db import models
from django.contrib.auth import get_user_model

class Question(models.Model):
    question_text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    answer_text = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer_text
