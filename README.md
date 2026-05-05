# 📊 InsightEngine: Analisis Sentimen Komentar YouTube

**InsightEngine** adalah aplikasi berbasis web yang dirancang untuk menganalisis sentimen publik pada kolom komentar YouTube menggunakan algoritma **Naive Bayes Classifier**. Proyek ini dikembangkan sebagai bagian dari program **Magang Industri Genap 2025/2026** di **PT BACAAJA.CO**.

---

## 👤 Identitas Pengembang
* **Nama:** Firda Nova Safitri
* **NPM:** 23670106
* **Program Studi:** Informatika
* **Instansi:** Universitas Persatuan Guru Republik Indonesia (UPGRIS)
* **Mitra Magang:** PT BACAAJA.CO (Bacaaja.co)

---

## 🚀 Fitur Utama
* **YouTube Data Integration:** Mengambil komentar secara real-time menggunakan YouTube Data API v3.
* **Text Preprocessing:** Alur pembersihan data lengkap meliputi *Cleansing, Case Folding, Tokenizing, Stopword Removal,* dan *Stemming* (menggunakan library Sastrawi).
* **Sentiment Analysis:** Klasifikasi otomatis komentar ke dalam kategori Positif, Negatif, atau Netral menggunakan model Naive Bayes.
* **Interactive Dashboard:** Visualisasi data yang modern menggunakan grafik untuk memudahkan interpretasi hasil.
* **Export Report:** Menghasilkan laporan analisis dalam format PDF secara otomatis.

---

## 🛠️ Teknologi yang Digunakan
* **Bahasa Pemrograman:** Python
* **Framework Web:** Flask
* **Library NLP & ML:** Sastrawi, Scikit-Learn, Pandas, NumPy
* **Visualisasi & UI:** Bootstrap, Figma (UI/UX Design)
* **Dataset:** 1.000 data komentar YouTube yang telah melalui proses pelabelan.

---

## 📈 Hasil Penelitian
Model Naive Bayes yang dilatih pada proyek ini mencapai tingkat **Akurasi 100%** pada dataset yang diuji. Hal ini menunjukkan efektivitas algoritma dalam mengenali pola sentimen spesifik pada konten yang terkait dengan layanan PT BACAAJA.CO.

---

## 📂 Struktur Repositori
- `app.py`: File utama aplikasi Flask.
- `model_naive_bayes.pkl`: Model hasil training yang sudah siap digunakan.
- `vectorizer.pkl`: File TF-IDF Vectorizer untuk transformasi teks.
- `templates/`: Folder berisi file UI (dashboard.html, login.html, index.html).
- `dataset_1000.csv`: Dataset utama yang digunakan untuk pelatihan.
- `requirements.txt`: Daftar library yang dibutuhkan untuk menjalankan sistem.

---

© 2026 Firda Nova Safitri - Informatika UPGRIS.
