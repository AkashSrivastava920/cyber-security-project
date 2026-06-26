import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Initializing Phishing Email Detection Model...\n")

# ==========================================
# 1. LOAD DATASET (Phishing vs Legitimate)
# ==========================================
# For this script to run immediately, we are using a mock dataset. 
# In a real-world scenario, you would load a massive CSV file like this:
# df = pd.read_csv('spam_dataset.csv')

data = {
    'text': [
        "Hey ABC, let's grab lunch tomorrow at 12.",
        "URGENT: Your bank account has been suspended. Click http://fake-login.com to verify.",
        "Meeting notes from yesterday's marketing sync are attached.",
        "WINNER! Claim your $1000 Walmart gift card now! Click here to claim.",
        "Can you review the attached invoice by Friday?",
        "Security Alert: Unauthorized login attempt. Reset your password at http://secure-update-alert-verify.com",
        "Don't forget to submit your timesheet before the end of the day.",
        "Your PayPal account is limited. Update your billing info at http://paypal-update-info.net",
        "Hi Mom, I'll be home late tonight for dinner.",
        "CONGRATULATIONS! You've been selected for a free iPhone 15. Provide your address here."
    ],
    'label': ["Safe", "Phishing", "Safe", "Phishing", "Safe", "Phishing", "Safe", "Phishing", "Safe", "Phishing"]
}

# Convert dictionary into a Pandas DataFrame
df = pd.DataFrame(data)

# ==========================================
# 2. EXTRACT FEATURES (URLs, Keywords, etc.)
# ==========================================
print("[*] Extracting text features using TF-IDF...")
# TfidfVectorizer converts text (and URLs) into a matrix of numbers based on word frequency and importance
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text']) # X represents our features (the email text)
y = df['label']                          # y represents our target (Safe or Phishing)

# Split data: 70% for training the model, 30% for testing it
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ==========================================
# 3. TRAIN THE MACHINE LEARNING MODEL
# ==========================================
print("[*] Training Naive Bayes Classifier...")
# Multinomial Naive Bayes is the industry standard for text/spam classification
model = MultinomialNB()
model.fit(X_train, y_train)

# ==========================================
# 4. CLASSIFY & DISPLAY ACCURACY / CONFUSION MATRIX
# ==========================================
print("\n--- MODEL EVALUATION ---")
# Ask the model to predict the labels for our 30% test data
y_pred = model.predict(X_test)

# Calculate Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Generate Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred, labels=["Safe", "Phishing"])
print("\nConfusion Matrix:")
print("                 Predicted Safe | Predicted Phishing")
print(f"Actual Safe     |      {conf_matrix[0][0]}         |        {conf_matrix[0][1]}")
print(f"Actual Phishing |      {conf_matrix[1][0]}         |        {conf_matrix[1][1]}")

# ==========================================
# 5. TEST IT YOURSELF
# ==========================================
print("\n--- TEST A CUSTOM EMAIL ---")
test_emails = [
    "Please find the project files attached for review.",
    "Click http://free-money.com immediately to secure your prize!"
]

# We must transform the new text using the exact same vectorizer we trained with
test_features = vectorizer.transform(test_emails)
predictions = model.predict(test_features)

for email, prediction in zip(test_emails, predictions):
    print(f"\nEmail: '{email}'")
    print(f"Classification: -> {prediction} <-")