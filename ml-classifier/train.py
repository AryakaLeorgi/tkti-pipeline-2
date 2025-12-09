#!/usr/bin/env python3
"""
Train the error classification models with model comparison.
Compares: Random Forest, Gradient Boosting, SVM, Logistic Regression, Decision Tree
"""

from training_data import get_all_training_data, get_category_counts
from model import ErrorClassifier

def main():
    print("=" * 70)
    print("    ERROR CLASSIFICATION MODEL TRAINING WITH COMPARISON")
    print("=" * 70)
    
    # Get training data
    data = get_all_training_data()
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(data)}")
    
    # Count by category
    counts = get_category_counts()
    print(f"\n📁 Samples per category:")
    for cat, count in sorted(counts.items()):
        fixable = "✅ fixable" if cat in ["syntax_error", "runtime_error", "test_failure"] else "❌ not fixable"
        print(f"   - {cat}: {count} ({fixable})")
    
    print("\n" + "=" * 70)
    print("    TRAINING WITH MODEL COMPARISON")
    print("=" * 70)
    
    # Train classifier with model comparison
    classifier = ErrorClassifier()
    classifier.train(data, compare_all=True)
    
    # Test with real-world examples
    print("\n" + "=" * 70)
    print("    TESTING WITH REAL-WORLD EXAMPLES")
    print("=" * 70)
    
    test_cases = [
        # Fixable errors
        "TypeError: Cannot read property 'map' of undefined",
        "SyntaxError: Unexpected token at line 42",
        "TypeError: /[A-Z]/.tset is not a function at UserAuth.validatePassword",
        "FAIL: 1 test failed in auth.test.js",
        "AssertionError: expected 'hello' to equal 'world'",
        # Non-fixable errors
        "npm ERR! 404 package not found",
        "ECONNREFUSED: Connection refused",
        "Missing environment variable API_KEY",
        "502 Bad Gateway nginx",
    ]
    
    print(f"\n{'Error Sample':<55} {'Category':<18} {'Fixable':<8} {'Conf':<6}")
    print("-" * 95)
    
    for test in test_cases:
        result = classifier.predict(test)
        short_test = test[:52] + "..." if len(test) > 55 else test
        fixable_str = "✅ Yes" if result["fixable"] else "❌ No"
        print(f"{short_test:<55} {result['category']:<18} {fixable_str:<8} {result['confidence']:.0%}")
    
    print("-" * 95)
    
    # Summary
    print(f"\n📈 Best Model Selected: {classifier.best_model_name.upper()}")
    print("✅ Training complete! Models saved to disk.")

if __name__ == "__main__":
    main()
