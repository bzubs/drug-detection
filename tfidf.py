import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("final.csv")
print(len(df))
df = df.drop_duplicates(subset=['text'])
print(len(df))
X = df["text"]
y = df["label"]   # should contain only 0 and 1

# TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_tfidf = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# Logistic Regression (binary classification)
clf = LogisticRegression(solver="lbfgs", max_iter=2000)
clf.fit(X_train, y_train)

# Predictions on test
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# ---------------------------
# Function for new input text
# ---------------------------
def predict_text(text):
    text_tfidf = vectorizer.transform([text])   # transform using same vectorizer
    prediction = clf.predict(text_tfidf)[0]
    proba = clf.predict_proba(text_tfidf)[0]    # [P(class 0), P(class 1)]
    return prediction, {"class_0": proba[0], "class_1": proba[1]}

# Example usage
new_text = "yo got some coke?"
label, scores = predict_text(new_text)
print("Prediction:", label)
print("Class Probabilities:", scores)
