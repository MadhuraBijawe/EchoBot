from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SupportTicket, SuggestedReply, Feedback, KnowledgeBase
from .serializers import SupportTicketSerializer, SuggestedReplySerializer, FeedbackSerializer, KnowledgeBaseSerializer
from .ml_service import MLService

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all().order_by('-created_at')
    serializer_class = SupportTicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save()
        
        # Generate suggestions
        ml_service = MLService()
        suggestions = ml_service.get_suggestions(ticket.description)
        
        for sugg in suggestions:
            SuggestedReply.objects.create(
                ticket=ticket,
                reply_text=sugg['reply_text'],
                confidence_score=sugg['confidence_score']
            )

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class KnowledgeBaseViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
