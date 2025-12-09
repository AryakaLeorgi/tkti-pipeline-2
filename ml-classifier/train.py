#!/usr/bin/env python3
"""
Train the error classification models.
Run this script to generate the model files.
"""

from training_data import get_all_training_data
from model import ErrorClassifier

def main():
    print("=" * 50)
    print("Training Error Classification Models")
    print("=" * 50)
    
    # Get training data
    data = get_all_training_data()
    print(f"\nLoaded {len(data)} training samples")
    
    # Count by category
    categories = {}
    for d in data:
        cat = d["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nSamples per category:")
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count}")
    
    # Train classifier
    classifier = ErrorClassifier()
    classifier.train(data)
    
    # Test with some examples
    print("\n" + "=" * 50)
    print("Testing trained models")
    print("=" * 50)
    
    test_cases = [
        "TypeError: Cannot read property 'map' of undefined",
        "SyntaxError: Unexpected token at line 42",
        "npm ERR! 404 package not found",
        "ECONNREFUSED: Connection refused",
        "AssertionError: expected true to be false",
        "Missing environment variable API_KEY",
    ]
    
    for test in test_cases:
        result = classifier.predict(test)
        print(f"\n'{test[:50]}...'")
        print(f"  → Category: {result['category']}")
        print(f"  → Fixable: {result['fixable']}")
        print(f"  → Priority: {result['priority']}")
        print(f"  → Confidence: {result['confidence']:.1%}")
    
    print("\n✅ Training complete! Models saved.")

if __name__ == "__main__":
    main()
