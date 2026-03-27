import pandas as pd
import pickle
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

os.makedirs("model", exist_ok=True)

data = pd.read_csv("dataset/spam.csv", sep="\t", names=["label","message"])

data['label'] = data['label'].map({'ham':0,'spam':1})

X = data['message']
y = data['label']

vectorizer = TfidfVectorizer(stop_words='english')

X_vector = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vector, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test,pred))

pickle.dump(model, open("model/model.pkl","wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl","wb"))

print("Model saved successfully")