import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'support_system.settings')
django.setup()

from api.models import KnowledgeBase

def populate_kb():
    data = [
        {
            "question": "How do I reset my password?",
            "answer": "To reset your password, go to the login page and click on 'Forgot Password'. Follow the instructions sent to your email.",
            "category": "Account"
        },
        {
            "question": "Where can I find my order status?",
            "answer": "You can track your order by logging into your account and visiting the 'My Orders' section.",
            "category": "Orders"
        },
        {
            "question": "What is your refund policy?",
            "answer": "We offer a full refund within 30 days of purchase if you are not satisfied with our product. Please contact support to initiate a return.",
            "category": "Returns"
        },
        {
            "question": "How do I change my subscription plan?",
            "answer": "Go to 'Account Settings' > 'Billing' and select 'Change Plan'. You can upgrade or downgrade at any time.",
            "category": "Billing"
        },
        {
            "question": "The app is crashing on startup",
            "answer": "Please try clearing your app cache and data. If the issue persists, reinstall the application and ensure you have the latest version.",
            "category": "Technical"
        },
        {
            "question": "Do you offer international shipping?",
            "answer": "Yes, we ship to over 100 countries. Shipping costs and times vary by location.",
            "category": "Shipping"
        },
        {
            "question": "How can I contact customer support?",
            "answer": "You can reach us via email at support@example.com or call our hotline at 1-800-123-4567.",
            "category": "General"
        }
    ]

    for item in data:
        KnowledgeBase.objects.get_or_create(
            question=item['question'],
            defaults={'answer': item['answer'], 'category': item['category']}
        )
    
    print(f"Successfully populated Knowledge Base with {len(data)} items.")

if __name__ == '__main__':
    populate_kb()
