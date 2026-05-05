import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 1. Load Dataset dan Model
try:
    df = pd.read_csv('dataset_1000.csv')
    with open('model_naive_bayes.pkl', 'rb') as f:
        model_nb = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("Berhasil memuat data dan model untuk pengujian.")
except Exception as e:
    print(f"Gagal memuat file: {e}")
    exit()

# 2. Persiapkan Data Uji (Testing Data)
# Kita ambil 20% dari dataset (200 baris) untuk diuji tingkat akurasinya
X = df['teks']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Proses Prediksi
# Mengubah teks uji menjadi vektor angka
X_test_vector = vectorizer.transform(X_test)
y_pred = model_nb.predict(X_test_vector)

# 4. Hitung Skor Akurasi
accuracy = accuracy_score(y_test, y_pred)
print("\n" + "="*30)
print(f"HASIL UJI AKURASI: {accuracy * 100:.2f}%")
print("="*30)

# 5. Laporan Detail (Precision, Recall, F1-Score)
print("\nLaporan Klasifikasi Detail:")
print(classification_report(y_test, y_pred, target_names=['Negatif', 'Positif']))

# 6. Confusion Matrix (Opsional untuk tabel laporan)
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))