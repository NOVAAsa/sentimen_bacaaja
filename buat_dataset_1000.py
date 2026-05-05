import pandas as pd
import random

# Data spesifik yang Anda berikan (Manual labeling)
raw_data = """
bodoh banget tindakannya,0
toxic banget komentarnya,0
hoax banget infonya gak jelas,0
salah sendiri kenapa melanggar aturan,0
rekomendasi banget buat ditonton,1
terima kasih infonya sangat membantu,1
keren abis informasinya,1
jos gandos pokoknya,1
mantap sekali pak bapak memang terbaik,1
nyesel nonton video ini buang kuota,0
... (masukkan semua baris teks yang Anda berikan di sini) ...
"""

# 1. Memproses data manual dari teks Anda
manual_data = []
for line in raw_data.strip().split('\n'):
    if ',' in line:
        teks, label = line.rsplit(',', 1)
        manual_data.append([teks.strip(), int(label.strip())])

# 2. Template untuk memperbanyak dataset (Data Augmentation)
pos_templates = [
    "mantap sekali pak {subjek} memang terbaik", "salut buat perjuangan bapak", 
    "keren informasinya sangat bermanfaat", "sehat selalu orang baik",
    "inspiratif banget kontennya", "setuju banget sama bapak ini",
    "terima kasih infonya sangat membantu", "pemimpin yang merakyat dan jujur",
    "masya allah baik sekali hatinya", "jos gandos pokoknya",
    "bangga punya sosok seperti beliau", "penjelasan yang sangat cerdas"
]

neg_templates = [
    "parah banget sih ini merugikan orang", "kecewa sama pelayanannya buruk",
    "dasar egois mau menangnya sendiri", "konten sampah gak mutu",
    "penipuan ini jangan dipercaya", "hoax banget infonya gak jelas",
    "bodoh banget tindakannya", "malu-maluin aja kelakuannya",
    "gak punya otak kali ya", "hancur sudah reputasinya"
]

subjek = ["ganjar", "petugas", "pengendara", "admin", "bapak", "sopir"]

generated_data = []
# Generate tambahan 500 data agar model lebih stabil
for _ in range(250):
    generated_data.append([random.choice(pos_templates).format(subjek=random.choice(subjek)), 1])
    generated_data.append([random.choice(neg_templates), 0])

# 3. Gabungkan Data Manual + Data Generated
final_data = manual_data + generated_data
random.shuffle(final_data)

# 4. Simpan ke CSV
df = pd.DataFrame(final_data, columns=['teks', 'label'])
df.to_csv('dataset_1000.csv', index=False)

print(f"Sukses! Total {len(df)} baris data berhasil disimpan ke dataset_1000.csv")