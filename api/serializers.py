from rest_framework import serializers
from .models import SupportTicket, SuggestedReply, Feedback, KnowledgeBase

class SuggestedReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedReply
        fields = ['id', 'reply_text', 'confidence_score', 'created_at']

class SupportTicketSerializer(serializers.ModelSerializer):
    suggestions = SuggestedReplySerializer(many=True, read_only=True)

    class Meta:
        model = SupportTicket
        fields = ['id', 'subject', 'description', 'status', 'created_at', 'suggestions']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'suggestion', 'is_helpful', 'comment', 'created_at']

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = ['id', 'question', 'answer', 'category']
