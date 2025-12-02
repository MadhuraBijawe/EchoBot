from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupportTicketViewSet, FeedbackViewSet, KnowledgeBaseViewSet

router = DefaultRouter()
router.register(r'tickets', SupportTicketViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'knowledge-base', KnowledgeBaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
