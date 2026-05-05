import webview
import re
import io
import pickle
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from googleapiclient.discovery import build
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from threading import Thread

# Import ReportLab untuk PDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
app.secret_key = 'bacaaja_key_secret'

# --- 1. KONFIGURASI API & MODEL ---
YOUTUBE_API_KEY = "AIzaSyAIiNj7Tow5i97A75wzSNOZ3SYrny_rtLQ"
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Load Model Naive Bayes
try:
    with open('model_naive_bayes.pkl', 'rb') as f:
        model_nb = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    print("Model Berhasil Dimuat.")
except Exception as e:
    print(f"Peringatan: Gagal memuat model! Error: {e}")

data_results = []

# --- 2. ENGINE TEXT MINING ---
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocess_text(text):
    clean = text.lower()
    clean = re.sub(r'<.*?>', '', clean) 
    clean = re.sub(r'http\S+|www\S+|https\S+', '', clean, flags=re.MULTILINE) 
    clean = re.sub(r'([a-z])\1{2,}', r'\1', clean) 
    clean = re.sub(r'[^\w\s]', '', clean) 
    stemmed = stemmer.stem(clean)
    return clean, stemmed

def get_sentiment(text_stemmed):
    try:
        text_vector = vectorizer.transform([text_stemmed])
        prediction = model_nb.predict(text_vector)[0]
        return "Positif" if prediction == 1 else "Negatif"
    except:
        return "Netral"

# --- 3. ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        # PENYESUAIAN KREDENSIAL: MORNOV / 23670106
        if user == 'MORNOV' and pw == '23670106':
            session['user'] = user
            return redirect(url_for('index'))
        
        return "Login gagal! Gunakan username MORNOV dan password NPM Anda."
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Menghapus session untuk keamanan
    session.clear() 
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user' not in session: 
        return redirect(url_for('login'))
        
    pos = sum(1 for d in data_results if d['label'] == 'Positif')
    neg = sum(1 for d in data_results if d['label'] == 'Negatif')
    net = sum(1 for d in data_results if d['label'] == 'Netral')
    
    return render_template('dashboard.html', 
                           posts=data_results, 
                           total=len(data_results), 
                           chart_data=[pos, neg, net], 
                           role=session['user'])

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'user' not in session: return redirect(url_for('login'))
    
    url = request.form.get('url')
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    
    if video_id_match:
        video_id = video_id_match.group(1)
        nextPageToken = None
        target_count = 200 # TARGET 200 KOMENTAR
        
        try:
            while len(data_results) < target_count:
                response = youtube.commentThreads().list(
                    part="snippet", 
                    videoId=video_id, 
                    maxResults=100, 
                    pageToken=nextPageToken,
                    textFormat="plainText"
                ).execute()
                
                for item in response.get('items', []):
                    if len(data_results) >= target_count: break
                    
                    text_asli = item['snippet']['topLevelComment']['snippet']['textDisplay']
                    clean, stem = preprocess_text(text_asli)
                    label = get_sentiment(stem)
                    
                    data_results.append({
                        'id_youtube': video_id, 
                        'comment_original': text_asli, 
                        'text_stem': stem, 
                        'label': label
                    })
                
                nextPageToken = response.get('nextPageToken')
                if not nextPageToken: break 
                
        except Exception as e:
            print(f"YouTube API Error: {e}")
            
    return redirect(url_for('index'))

@app.route('/reset')
def reset_data():
    if 'user' not in session: return redirect(url_for('login'))
    global data_results
    data_results = []
    return redirect(url_for('index'))

@app.route('/download')
def download():
    if 'user' not in session: return redirect(url_for('login'))
    if not data_results: 
        return "Gagal: Tidak ada data hasil analisis untuk diekspor.", 400
        
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        elements = []
        styles = getSampleStyleSheet()
        
        style_isi = ParagraphStyle('style_isi', fontSize=8, leading=10, wordWrap='CJK')
        elements.append(Paragraph("<b>LAPORAN ANALISIS SENTIMEN YOUTUBE - PT BACAAJA.CO</b>", styles['Title']))
        elements.append(Paragraph(f"Oleh: {session.get('user', 'Firda Nova Safitri')}", styles['Normal']))
        elements.append(Spacer(1, 15))

        data = [["No", "ID Video", "Komentar Asli", "Hasil Stemming", "Label"]]
        for i, item in enumerate(data_results, 1):
            comment_safe = item['comment_original'].encode('ascii', 'ignore').decode('ascii')
            stem_safe = item['text_stem'].encode('ascii', 'ignore').decode('ascii')
            
            data.append([
                str(i), 
                item['id_youtube'], 
                Paragraph(comment_safe, style_isi), 
                Paragraph(stem_safe, style_isi), 
                item['label']
            ])

        table = Table(data, colWidths=[30, 80, 280, 280, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff758c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='Laporan_Sentiment_Bacaaja.pdf')
    except Exception as e:
        return f"Terjadi kesalahan teknis saat ekspor PDF: {str(e)}", 500

def run_flask():
    app.run(port=8080, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Menjalankan Flask di background thread
    Thread(target=run_flask, daemon=True).start()
    
    # Membuka window aplikasi desktop dengan kredensial baru
    webview.create_window('Insight Engine - Naive Bayes', 'http://127.0.0.1:8080/login', width=1200, height=800)
    webview.start()