import joblib

# Load model and metadata
pipeline = joblib.load('spam_classifier.pkl')
meta = joblib.load('model_metadata.pkl')

print("="*60)
print("SPAM CLASSIFIER MODEL TEST")
print("="*60)
print(f"Model: {meta['model_name']}")
print(f"Accuracy: {meta['accuracy']:.4f}")
print(f"F1-Score: {meta['f1_score']:.4f}")
print(f"Training Samples: {meta['training_samples']}")
print("="*60)

# Test messages (mix of real spam and ham examples)
test_messages = [
    # Real spam examples
    "URGENT! Your mobile number has been awarded £2000 prize GUARANTEED. Call 09061790121 from land line. Claim 3030. Valid 12hrs only",
    "FREE entry into our £250 weekly competition just text the word WIN to 80086 NOW. 18 T&C apply",
    "Congratulations! You've won a FREE iPhone 15! Click here to claim: www.fake-prize.com",
    "Your account has been suspended due to suspicious activity. Verify now: bit.ly/verify-account",
    "WINNER!! As a valued network customer you have been selected to receive a £900 prize reward! Call 09061701461. Claim code KL341.",

    # Real ham examples
    "Hey, how are you doing? Let's catch up this weekend.",
    "Hi mom, just wanted to let you know I got home safely. Love you!",
    "Meeting scheduled for tomorrow at 2 PM in conference room B.",
    "Thanks for the help with the project. It was really appreciated.",
    "Can you please send me the report when you get a chance?",
    "Happy birthday! Hope you have a great day!",
    "The weather is nice today, perfect for a walk in the park.",
    "Don't forget to pick up milk on your way home.",
    "Looking forward to our vacation next month!",
    "Just finished reading that book you recommended. It was excellent!"
]

print("\nTESTING ON UNSEEN DATA:")
print("-" * 60)

spam_count = 0
ham_count = 0

for i, msg in enumerate(test_messages, 1):
    prediction = pipeline.predict([msg])[0]
    probabilities = pipeline.predict_proba([msg])[0]

    label = "SPAM ⚠️" if prediction == 1 else "HAM ✓"
    confidence = probabilities[prediction]

    if prediction == 1:
        spam_count += 1
    else:
        ham_count += 1

    print(f"\n{i}. {label}")
    print(f"   Message: {msg[:60]}{'...' if len(msg) > 60 else ''}")
    print(f"   Confidence: {confidence:.3f}")
    print(f"   Probabilities: Ham={probabilities[0]:.3f}, Spam={probabilities[1]:.3f}")

print("\n" + "="*60)
print("SUMMARY:")
print(f"Total messages tested: {len(test_messages)}")
print(f"Predicted as SPAM: {spam_count}")
print(f"Predicted as HAM: {ham_count}")
print(".1f")
print("="*60)