"""
ML Error Classifier Model with Multiple Algorithms
Uses TF-IDF + Multiple classifiers for comparison:
- Random Forest
- Gradient Boosting  
- SVM (Support Vector Machine)
- Logistic Regression
- Decision Tree
"""

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np

# Model file paths
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
CATEGORY_MODEL_PATH = os.path.join(MODEL_DIR, "category_model.joblib")
FIXABLE_MODEL_PATH = os.path.join(MODEL_DIR, "fixable_model.joblib")
PRIORITY_MODEL_PATH = os.path.join(MODEL_DIR, "priority_model.joblib")
BEST_MODEL_INFO_PATH = os.path.join(MODEL_DIR, "best_model_info.joblib")

# Available models for comparison
AVAILABLE_MODELS = {
    "random_forest": lambda: RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "gradient_boosting": lambda: GradientBoostingClassifier(n_estimators=100, random_state=42),
    "svm": lambda: SVC(kernel='rbf', probability=True, random_state=42),
    "logistic_regression": lambda: LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
    "decision_tree": lambda: DecisionTreeClassifier(random_state=42, max_depth=10),
}

class ErrorClassifier:
    """
    ML-based error classifier that predicts:
    - Error category (syntax, runtime, test, dependency, config, network)
    - Whether error is auto-fixable
    - Priority level (high, medium, low)
    
    Supports multiple algorithms with performance comparison.
    """
    
    def __init__(self):
        self.category_model = None
        self.fixable_model = None
        self.priority_model = None
        self.best_model_name = "random_forest"
        self.model_scores = {}
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
            if os.path.exists(BEST_MODEL_INFO_PATH):
                info = joblib.load(BEST_MODEL_INFO_PATH)
                self.best_model_name = info.get("best_model", "random_forest")
                self.model_scores = info.get("scores", {})
        except Exception as e:
            print(f"Warning: Could not load models: {e}")
    
    def is_trained(self) -> bool:
        """Check if all models are trained."""
        return all([
            self.category_model is not None,
            self.fixable_model is not None,
            self.priority_model is not None
        ])
    
    def compare_models(self, texts: list, labels: list, task_name: str = "category"):
        """
        Compare all available models and return performance metrics.
        
        Args:
            texts: List of text samples
            labels: List of corresponding labels
            task_name: Name of the classification task
            
        Returns:
            Dict with model names and their scores
        """
        print(f"\n{'='*60}")
        print(f"Comparing Models for: {task_name}")
        print(f"{'='*60}")
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
        
        results = {}
        best_score = 0
        best_model_name = None
        best_pipeline = None
        
        for model_name, model_fn in AVAILABLE_MODELS.items():
            print(f"\n--- {model_name.upper()} ---")
            
            # Create pipeline
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=1000)),
                ('clf', model_fn())
            ])
            
            # Train
            pipeline.fit(X_train, y_train)
            
            # Evaluate
            y_pred = pipeline.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(pipeline, texts, labels, cv=5)
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            
            print(f"Test Accuracy: {accuracy:.2%}")
            print(f"Cross-Val Accuracy: {cv_mean:.2%} (+/- {cv_std:.2%})")
            
            results[model_name] = {
                "test_accuracy": accuracy,
                "cv_mean": cv_mean,
                "cv_std": cv_std,
                "pipeline": pipeline
            }
            
            # Track best model
            if cv_mean > best_score:
                best_score = cv_mean
                best_model_name = model_name
                best_pipeline = pipeline
        
        # Summary table
        print(f"\n{'='*60}")
        print(f"MODEL COMPARISON SUMMARY - {task_name}")
        print(f"{'='*60}")
        print(f"{'Model':<25} {'Test Acc':>12} {'CV Mean':>12} {'CV Std':>10}")
        print("-" * 60)
        
        for name, data in sorted(results.items(), key=lambda x: x[1]['cv_mean'], reverse=True):
            marker = " ★ BEST" if name == best_model_name else ""
            print(f"{name:<25} {data['test_accuracy']:>11.2%} {data['cv_mean']:>11.2%} {data['cv_std']:>9.2%}{marker}")
        
        print("-" * 60)
        
        return results, best_model_name, best_pipeline
    
    def train(self, training_data: list, compare_all: bool = True):
        """
        Train all classification models.
        
        Args:
            training_data: List of dicts with 'text', 'category', 'fixable', 'priority'
            compare_all: Whether to compare all models
        """
        texts = [d["text"] for d in training_data]
        categories = [d["category"] for d in training_data]
        fixable = [d["fixable"] for d in training_data]
        priorities = [d["priority"] for d in training_data]
        
        model_scores = {}
        
        # Compare and train category classifier
        if compare_all:
            results, best_name, best_pipeline = self.compare_models(texts, categories, "Category Classification")
            self.category_model = best_pipeline
            model_scores["category"] = {k: {"cv_mean": v["cv_mean"], "test_acc": v["test_accuracy"]} 
                                        for k, v in results.items()}
            self.best_model_name = best_name
        else:
            print("Training category classifier with Random Forest...")
            self.category_model = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=1000)),
                ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
            ])
            self.category_model.fit(texts, categories)
        
        # Compare and train fixable classifier
        if compare_all:
            results, _, best_pipeline = self.compare_models(texts, fixable, "Fixable Classification")
            self.fixable_model = best_pipeline
            model_scores["fixable"] = {k: {"cv_mean": v["cv_mean"], "test_acc": v["test_accuracy"]} 
                                       for k, v in results.items()}
        else:
            print("Training fixable classifier...")
            self.fixable_model = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=1000)),
                ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
            ])
            self.fixable_model.fit(texts, fixable)
        
        # Train priority classifier (simpler, often doesn't need comparison)
        print("\nTraining priority classifier...")
        self.priority_model = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=500)),
            ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        self.priority_model.fit(texts, priorities)
        
        # Save models and info
        self._save_models()
        self.model_scores = model_scores
        
        # Save best model info
        joblib.dump({
            "best_model": self.best_model_name,
            "scores": model_scores
        }, BEST_MODEL_INFO_PATH)
        
        print("\n✅ All models trained and saved!")
    
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
            "confidence": round(float(confidence), 3),
            "model_used": self.best_model_name
        }
    
    def evaluate(self, test_data: list):
        """Evaluate model performance on test data."""
        texts = [d["text"] for d in test_data]
        categories = [d["category"] for d in test_data]
        
        predictions = self.category_model.predict(texts)
        print("\nCategory Classification Report:")
        print(classification_report(categories, predictions))
        
        print("\nConfusion Matrix:")
        cm = confusion_matrix(categories, predictions)
        print(cm)


# Global classifier instance
_classifier = None

def get_classifier() -> ErrorClassifier:
    """Get or create the global classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = ErrorClassifier()
    return _classifier
