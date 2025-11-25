import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

df = pd.read_csv("dataset.csv")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['question'])

model = {
    "vectorizer": vectorizer,
    "X": X,
    "answers": df['answer'].tolist(),
    "questions": df['question'].tolist()
}

pickle.dump(model, open("model.pkl", "wb"))
print("Model trained and saved successfully!")