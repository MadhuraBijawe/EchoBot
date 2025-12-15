import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import KnowledgeBase, SuggestedReply

class MLService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.kb_data = None
        self.tfidf_matrix = None
        self._load_data()

    def _load_data(self):
        """Load KnowledgeBase data and train vectorizer"""
        kb_items = KnowledgeBase.objects.all()
        if not kb_items.exists():
            self.kb_data = pd.DataFrame(columns=['id', 'question', 'answer'])
            return

        data = []
        for item in kb_items:
            data.append({
                'id': item.id,
                'question': item.question,
                'answer': item.answer
            })
        
        self.kb_data = pd.DataFrame(data)
        if not self.kb_data.empty:
            # Combine question and answer for better matching context
            self.kb_data['combined_text'] = self.kb_data['question'] + " " + self.kb_data['answer']
            self.tfidf_matrix = self.vectorizer.fit_transform(self.kb_data['combined_text'])

    def get_suggestions(self, ticket_text, top_n=3):
        """Get top N suggested replies for a given ticket text"""
        # Reload data if needed (simple caching strategy)
        # In production, you'd want a more robust update mechanism
        self._load_data()
        
        if self.kb_data is None or self.kb_data.empty:
            return []

        # Transform ticket text
        ticket_vector = self.vectorizer.transform([ticket_text])

        # Calculate similarity
        cosine_sim = cosine_similarity(ticket_vector, self.tfidf_matrix).flatten()

        # Get top N indices
        related_docs_indices = cosine_sim.argsort()[:-top_n-1:-1]

        suggestions = []
        for idx in related_docs_indices:
            score = cosine_sim[idx]
            if score > 0.1:  # Minimum threshold
                suggestions.append({
                    'reply_text': self.kb_data.iloc[idx]['answer'],
                    'confidence_score': float(score)
                })
        
        return suggestions
