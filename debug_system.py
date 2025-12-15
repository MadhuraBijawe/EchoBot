import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'support_system.settings')
django.setup()

from api.models import KnowledgeBase, SupportTicket
from api.ml_service import MLService

def check_system():
    print("--- Checking Database ---")
    try:
        kb_count = KnowledgeBase.objects.count()
        print(f"KnowledgeBase items: {kb_count}")
        if kb_count == 0:
            print("WARNING: KnowledgeBase is empty! Suggestions will not work.")
    except Exception as e:
        print(f"ERROR accessing database: {e}")
        return

    print("\n--- Testing ML Service ---")
    try:
        ml = MLService()
        print("ML Service initialized.")
        
        test_query = "How do I return an item?"
        print(f"Testing query: '{test_query}'")
        
        suggestions = ml.get_suggestions(test_query)
        print(f"Suggestions found: {len(suggestions)}")
        for s in suggestions:
            print(f"- {s['reply_text'][:50]}... (Score: {s['confidence_score']:.2f})")
            
    except Exception as e:
        print(f"ERROR in ML Service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_system()
