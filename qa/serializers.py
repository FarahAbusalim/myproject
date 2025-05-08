from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'user', 'created_at']

    def validate_answer_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Answer text cannot be empty or contain only whitespace.")
        return value


class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'user', 'created_at', 'answers']

    def get_answers(self, obj):
        ordered_answers = obj.answers.order_by('-created_at')
        return AnswerSerializer(ordered_answers, many=True).data

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty or contain only whitespace.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty or contain only whitespace.")
        return value
