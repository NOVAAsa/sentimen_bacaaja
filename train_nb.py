import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# 1. Load Dataset
try:
    df = pd.read_csv('dataset_1000.csv') 
    # Menghapus data yang kosong (NaN) agar tidak error saat fit_transform
    df = df.dropna(subset=['teks'])
    print(f"Berhasil membaca {len(df)} baris dataset.")[cite: 1]
except FileNotFoundError:
    print("Error: File dataset_1000.csv tidak ditemukan!")
    exit()

# 2. Vektorisasi TF-IDF dengan N-Gram
# max_features membantu membatasi kata yang tidak penting
# ngram_range(1,2) menangkap konteks "maaf tapi", "hukum berat", dll
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(df['teks']) 
y = df['label'] 

# 3. Training Naive Bayes
# alpha=0.1 (Laplace Smoothing) membantu model menangani kata yang belum pernah dilihat
model_nb = MultinomialNB(alpha=0.1)
model_nb.fit(X, y)[cite: 1]

# 4. Simpan Model & Vectorizer
with open('model_naive_bayes.pkl', 'wb') as f:
    pickle.dump(model_nb, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Sukses! Model Naive Bayes terbaru dengan N-Gram siap digunakan.")[cite: 1]