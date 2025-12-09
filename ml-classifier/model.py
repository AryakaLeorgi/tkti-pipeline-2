"""
ML Error Classifier Model
Uses TF-IDF + Random Forest for classification
"""

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

# Model file paths
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORY_MODEL_PATH = os.path.join(MODEL_DIR, "category_model.joblib")
FIXABLE_MODEL_PATH = os.path.join(MODEL_DIR, "fixable_model.joblib")
PRIORITY_MODEL_PATH = os.path.join(MODEL_DIR, "priority_model.joblib")

class ErrorClassifier:
    """
    ML-based error classifier that predicts:
    - Error category (syntax, runtime, test, dependency, config, network)
    - Whether error is auto-fixable
    - Priority level (high, medium, low)
    """
    
    def __init__(self):
        self.category_model = None
        self.fixable_model = None
        self.priority_model = None
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models if they exist."""
        try:
            if os.path.exists(CATEGORY_MODEL_PATH):
                self.category_model = joblib.load(CATEGORY_MODEL_PATH)
            if os.path.exists(FIXABLE_MODEL_PATH):
                self.fixable_model = joblib.load(FIXABLE_MODEL_PATH)
            if os.path.exists(PRIORITY_MODEL_PATH):
                self.priority_model = joblib.load(PRIORITY_MODEL_PATH)
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
    
    def is_trained(self) -> bool:
        """Check if all models are trained."""
        return all([
            self.category_model is not None,
            self.fixable_model is not None,
            self.priority_model is not None
        ])
    
    def train(self, training_data: list):
        """
        Train all classification models.
        
        Args:
            training_data: List of dicts with 'text', 'category', 'fixable', 'priority'
        """
        texts = [d["text"] for d in training_data]
        categories = [d["category"] for d in training_data]
        fixable = [d["fixable"] for d in training_data]
        priorities = [d["priority"] for d in training_data]
        
        # Train category classifier
        print("Training category classifier...")
        self.category_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=500)),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        self.category_model.fit(texts, categories)
        
        # Train fixable classifier
        print("Training fixable classifier...")
        self.fixable_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=500)),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        self.fixable_model.fit(texts, fixable)
        
        # Train priority classifier
        print("Training priority classifier...")
        self.priority_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=500)),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        self.priority_model.fit(texts, priorities)
        
        # Save models
        self._save_models()
        print("All models trained and saved!")
    
    def _save_models(self):
        """Save trained models to disk."""
        joblib.dump(self.category_model, CATEGORY_MODEL_PATH)
        joblib.dump(self.fixable_model, FIXABLE_MODEL_PATH)
        joblib.dump(self.priority_model, PRIORITY_MODEL_PATH)
    
    def predict(self, error_log: str) -> dict:
        """
        Classify an error log.
        
        Args:
            error_log: The error log text to classify
            
        Returns:
            Dict with category, fixable, priority, and confidence
        """
        if not self.is_trained():
            return {
                "category": "unknown",
                "fixable": False,
                "priority": "medium",
                "confidence": 0.0,
                "error": "Models not trained"
            }
        
        # Get predictions
        category = self.category_model.predict([error_log])[0]
        fixable = self.fixable_model.predict([error_log])[0]
        priority = self.priority_model.predict([error_log])[0]
        
        # Get confidence (probability of predicted class)
        category_proba = np.max(self.category_model.predict_proba([error_log]))
        fixable_proba = np.max(self.fixable_model.predict_proba([error_log]))
        
        # Average confidence
        confidence = (category_proba + fixable_proba) / 2
        
        return {
            "category": category,
            "fixable": bool(fixable),
            "priority": priority,
            "confidence": round(float(confidence), 3)
        }
    
    def evaluate(self, test_data: list):
        """Evaluate model performance on test data."""
        texts = [d["text"] for d in test_data]
        categories = [d["category"] for d in test_data]
        
        predictions = self.category_model.predict(texts)
        print("\nCategory Classification Report:")
        print(classification_report(categories, predictions))


# Global classifier instance
_classifier = None

def get_classifier() -> ErrorClassifier:
    """Get or create the global classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = ErrorClassifier()
    return _classifier
