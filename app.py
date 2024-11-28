from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np
import os
from PIL import Image
import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Konfigurasi Aplikasi
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    
    # Cloud SQL Connection Information
    CLOUD_SQL_CONNECTION_NAME = os.environ.get('CLOUD_SQL_CONNECTION_NAME', 'fourth-walker-434012:u9:asia-southeast2:appdatabase')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'k3r3n')
    DB_NAME = os.environ.get('DB_NAME', 'appdatabase')
    DB_HOST = os.environ.get('DB_HOST', '34.101.161.175')  # Public IP address
    
    # Database URI for Public IP connection
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Inisialisasi aplikasi dan konfigurasi
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Model untuk menyimpan riwayat
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # user_id bisa nullable jika tidak digunakan
    filename = db.Column(db.String(100), nullable=False)
    predictions_skin_conditions = db.Column(db.String(200), nullable=False)
    predictions_skin_type = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Muat model
model_kondisi_kulit = load_model('skin_conditions_model_2.h5')  # Model untuk kondisi kulit
model_tipe_kulit = load_model('skin_type_model.h5')  # Model untuk tipe kulit

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))  # Ubah ukuran gambar sesuai kebutuhan model
    img_array = np.array(img) / 255.0  # Normalisasi
    img_array = np.expand_dims(img_array, axis=0)  # Tambahkan dimensi batch
    return img_array

@app.route('/')
def home():
    return "Selamat datang di API Prediksi Kulit!"

@app.route('/prediksi_kulit', methods=['POST'])
def prediksi_kulit():
    if 'file' not in request.files:
        return jsonify({'error': 'Tidak ada file yang diunggah'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Tidak ada file yang dipilih'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipe file tidak diizinkan'}), 400
    
    user_id = request.form.get('user_id')  # Ambil user_id dari form data

    # Validasi user_id
    if user_id is None or user_id == '':
        return jsonify({'error': 'user_id tidak boleh kosong'}), 400

    # Simpan file dengan nama unik
    unique_filename = f"{uuid.uuid4()}.{file.filename.rsplit('.', 1)[1].lower()}"
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(img_path)

    try:
        # Proses gambar untuk model kondisi kulit
        img_array = preprocess_image(img_path)
        predictions_kondisi = model_kondisi_kulit.predict(img_array)

        # Mendapatkan probabilitas untuk setiap kelas
        one_hot_output_kondisi = predictions_kondisi[0].tolist()
        class_labels_kondisi = ['Acne', 'Eye Bags']  # Label untuk kondisi kulit

        # Format output untuk kondisi kulit
        predictions_output_kondisi = ", ".join([f"{label}: {prob:.2f}" for label, prob in zip(class_labels_kondisi, one_hot_output_kondisi)])

        # Proses gambar untuk model tipe kulit
        predictions_tipe = model_tipe_kulit.predict(img_array)
        one_hot_output_tipe = predictions_tipe[0].tolist()
        class_labels_tipe = ['Oily', 'Normal', 'Dry']  # Label untuk tipe kulit

        # Format output untuk tipe kulit
        predictions_output_tipe = ", ".join([f"{label}: {prob:.2f}" for label, prob in zip(class_labels_tipe, one_hot_output_tipe)])

        # Simpan data ke database
        new_history = History(
            user_id=user_id,  # Pastikan user_id tidak None
            filename=unique_filename,
            predictions_skin_conditions=predictions_output_kondisi,
            predictions_skin_type=predictions_output_tipe
        )
        db.session.add(new_history)
        db.session.commit()

        return jsonify({
            'filename': unique_filename,
            'predictions_skin_conditions': predictions_output_kondisi,
            'predictions_skin_type': predictions_output_tipe
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/history', methods=['GET'])
def get_history():
    try:
        # Ambil semua entri dari tabel History
        histories = History.query.all()
        results = []

        for history in histories:
            results.append({
                'id': history.id,
                'user_id': history.user_id,
                'filename': history.filename,
                'predictions_skin_conditions': history.predictions_skin_conditions,
                'predictions_skin_type': history.predictions_skin_type,
                'timestamp': history.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_history/<int:id>', methods=['DELETE'])
def delete_history(id):
    try:
        # Cari entri berdasarkan ID
        history_entry = History.query.get(id)
        
        if not history_entry:
            return jsonify({'error': 'Riwayat tidak ditemukan'}), 404
        
        # Hapus entri dari database
        db.session.delete(history_entry)
        db.session.commit()
        
        return jsonify({'message': 'Riwayat berhasil dihapus'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Buat database dan tabel jika belum ada
    with app.app_context():
        db.create_all()
    app.run(debug=True)

       