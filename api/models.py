from django.db import models

class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('pending', 'Pending'),
    ]

    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.subject}"

class KnowledgeBase(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]

class SuggestedReply(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='suggestions')
    reply_text = models.TextField()
    confidence_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion for #{self.ticket.id} ({self.confidence_score:.2f})"

class Feedback(models.Model):
    suggestion = models.ForeignKey(SuggestedReply, on_delete=models.CASCADE, related_name='feedback')
    is_helpful = models.BooleanField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Suggestion #{self.suggestion.id}"
