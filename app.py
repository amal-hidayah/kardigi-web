import os
import zipfile
import shutil
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from functools import wraps
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia_dapur_kardigi_2025_secure'

# --- 1. DEFINISI BASE_DIR (PINDAH KE ATAS) ---
# Didefinisikan di awal agar bisa dipakai di config database & folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# --- 2. KONFIGURASI DATABASE ---
# Menggunakan path absolut agar file .db tetap terbaca di server Azure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'amaljaya.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 3. KONFIGURASI FOLDER ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
DEMO_FOLDER = os.path.join(BASE_DIR, 'static/demos')
CV_FOLDER = os.path.join(BASE_DIR, 'static/files_cv')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEMO_FOLDER'] = DEMO_FOLDER
app.config['CV_FOLDER'] = CV_FOLDER

# Pastikan folder tersedia otomatis
for folder in [UPLOAD_FOLDER, DEMO_FOLDER, CV_FOLDER]:
    if not os.path.exists(folder): os.makedirs(folder)

# --- CONFIG ADMIN ---
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'kardigi123'
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename, extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_klien = db.Column(db.String(100))
    whatsapp = db.Column(db.String(20))
    jenis_jasa = db.Column(db.String(50))
    deskripsi = db.Column(db.Text)

class Referensi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    layanan_id = db.Column(db.String(50)) 
    kategori = db.Column(db.String(20))
    judul = db.Column(db.String(100))
    deskripsi = db.Column(db.Text)
    gambar = db.Column(db.String(200))
    file_path = db.Column(db.String(200))
    demo_folder = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

# --- DATA STATIS LAYANAN ---
DATA_LAYANAN = [
    {'id': 'company-profile', 'kategori': 'website', 'judul': 'Website Company Profile', 'deskripsi': 'Desain elegan untuk kredibilitas PT/CV.', 'gambar': 'web_compro.jpg'},
    {'id': 'toko-online', 'kategori': 'website', 'judul': 'Toko Online UMKM', 'deskripsi': 'Fitur keranjang belanja & checkout WA.', 'gambar': 'web_toko.jpg'},
    {'id': 'web-sekolah', 'kategori': 'website', 'judul': 'Website Sekolah', 'deskripsi': 'Portal akademik & PPDB Online.', 'gambar': 'web_sekolah.jpg'},
    {'id': 'cv-ats', 'kategori': 'cv', 'judul': 'CV ATS Friendly', 'deskripsi': 'Lolos sistem HRD & terbaca mesin.', 'gambar': 'cv_ats.jpg'},
    {'id': 'cv-kreatif', 'kategori': 'cv', 'judul': 'CV Kreatif', 'deskripsi': 'Desain visual menarik & estetik.', 'gambar': 'cv_kreatif.jpg'},
    {'id': 'surat-lamaran', 'kategori': 'cv', 'judul': 'Surat Lamaran', 'deskripsi': 'Kata-kata profesional pemikat HRD.', 'gambar': 'cv_english.jpg'}
]

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash("Silakan login terlebih dahulu!", "warning")
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTE LOGIN & LOGOUT ---
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash("Selamat datang, Bos!", "success")
            return redirect(url_for('admin_page'))
        else:
            flash("Username atau Password salah!", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("Anda berhasil logout.", "info")
    return redirect(url_for('login_page'))

# --- ROUTE PUBLIC ---
@app.route('/')
def home(): return render_template('index.html')

@app.route('/katalog')
def katalog_home(): return render_template('katalog_home.html')

@app.route('/katalog/<kategori_pilihan>')
def katalog_detail(kategori_pilihan):
    items = [item for item in DATA_LAYANAN if item['kategori'] == kategori_pilihan]
    judul = "Koleksi Website" if kategori_pilihan == 'website' else "Koleksi CV & Lamaran"
    return render_template('katalog_list.html', items=items, judul=judul, kategori=kategori_pilihan)

@app.route('/referensi/<id_layanan>')
def showcase_page(id_layanan):
    layanan_info = next((item for item in DATA_LAYANAN if item['id'] == id_layanan), None)
    if not layanan_info: return "Layanan tidak ditemukan", 404
    daftar_referensi = Referensi.query.filter_by(layanan_id=id_layanan).all()
    return render_template('showcase.html', layanan=layanan_info, referensi=daftar_referensi)

@app.route('/generator')
def cv_generator():
    return render_template('generator_cv.html')

# --- ROUTE ADMIN ---
@app.route('/admin')
@login_required
def admin_page():
    pesanan = Order.query.order_by(Order.id.desc()).all()
    referensi = Referensi.query.order_by(Referensi.id.desc()).all()
    return render_template('admin.html', pesanan=pesanan, referensi=referensi, layanan=DATA_LAYANAN)

@app.route('/admin/upload', methods=['POST'])
@login_required
def upload_referensi():
    if request.method == 'POST':
        layanan_id = request.form.get('layanan_id')
        judul = request.form.get('judul')
        deskripsi = request.form.get('deskripsi')
        kategori_item = next((item['kategori'] for item in DATA_LAYANAN if item['id'] == layanan_id), 'website')

        file_img = request.files.get('gambar')
        filename_img = None
        if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
            filename_img = secure_filename(file_img.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_img)
            
            # --- Optimasi Gambar Sebelum Simpan ---
            img = Image.open(file_img)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            if img.width > 1200:
                img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            img.save(filepath, optimize=True, quality=75)
        else:
            flash("Thumbnail wajib diupload!", "danger"); return redirect(url_for('admin_page'))

        file_project = request.files.get('file_zip')
        filename_project = None
        folder_demo_name = None

        if file_project and file_project.filename != '':
            filename_project = secure_filename(file_project.filename)
            if kategori_item == 'website' and filename_project.endswith('.zip'):
                folder_name = filename_project.rsplit('.', 1)[0]
                target_extract_path = os.path.join(app.config['DEMO_FOLDER'], folder_name)
                if os.path.exists(target_extract_path): shutil.rmtree(target_extract_path)
                try:
                    # --- Ekstraksi ZIP untuk Demo Website ---
                    with zipfile.ZipFile(file_project, 'r') as zip_ref: zip_ref.extractall(target_extract_path)
                    if not os.path.exists(os.path.join(target_extract_path, 'index.html')):
                        subitems = os.listdir(target_extract_path)
                        if len(subitems) == 1 and os.path.isdir(os.path.join(target_extract_path, subitems[0])):
                            nested_folder = os.path.join(target_extract_path, subitems[0])
                            for item in os.listdir(nested_folder): shutil.move(os.path.join(nested_folder, item), target_extract_path)
                            os.rmdir(nested_folder)
                    folder_demo_name = folder_name
                except zipfile.BadZipFile: flash("File ZIP rusak!", "danger"); return redirect(url_for('admin_page'))
            elif kategori_item == 'cv': 
                file_project.save(os.path.join(app.config['CV_FOLDER'], filename_project))

        baru = Referensi(layanan_id=layanan_id, kategori=kategori_item, judul=judul, deskripsi=deskripsi, gambar=filename_img, file_path=filename_project, demo_folder=folder_demo_name)
        db.session.add(baru); db.session.commit()
        flash("Upload sukses!", "success")
    return redirect(url_for('admin_page'))

@app.route('/hapus_referensi/<int:id>')
@login_required
def hapus_referensi(id):
    item = Referensi.query.get(id)
    if item:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.gambar))
        except: pass
        try: shutil.rmtree(os.path.join(app.config['DEMO_FOLDER'], item.demo_folder))
        except: pass
        try: os.remove(os.path.join(app.config['CV_FOLDER'], item.file_path))
        except: pass
        db.session.delete(item); db.session.commit()
        flash("Data dihapus.", "success")
    return redirect(url_for('admin_page'))

@app.route('/hapus_order/<int:id>')
@login_required
def hapus_pesanan(id):
    item = Order.query.get(id); db.session.delete(item); db.session.commit()
    return redirect(url_for('admin_page'))

@app.route('/order', methods=['GET', 'POST'])
def order():
    referensi_pilihan = request.args.get('ref', '')
    if request.method == 'POST':
        nama = request.form.get('nama'); wa = request.form.get('whatsapp'); jasa = request.form.get('service'); design_ref = request.form.get('design_ref'); ket_umum = request.form.get('keterangan')
        detail_msg = ""
        if jasa == 'website':
            detail_msg = f"--- DATA WEBSITE ---\n🏢 Bisnis: {request.form.get('web_bisnis', '-')}\n🌐 Domain: {request.form.get('web_domain', '-')}\n🎨 Warna: {request.form.get('web_warna', '-')}"
        elif jasa == 'cv':
            detail_msg = f"--- DATA CV ---\n💼 Posisi: {request.form.get('cv_posisi', '-')}\n🎓 Pendidikan: {request.form.get('cv_pendidikan', '-')}\n🏢 Pengalaman: {request.form.get('cv_pengalaman', '-')}\n⭐ Skill: {request.form.get('cv_skill', '-')}"
        
        deskripsi_lengkap = f"Design Ref: {design_ref}\n\n{detail_msg}\n\nCatatan: {ket_umum}"
        pesanan_baru = Order(nama_klien=nama, whatsapp=wa, jenis_jasa=jasa, deskripsi=deskripsi_lengkap)
        db.session.add(pesanan_baru); db.session.commit()
        
        nomor_admin = "6289509951772"
        pesan_wa = f"Halo Admin KARDIGI, order baru!\n\n👤 *DATA PEMESAN*\nNama: {nama}\nWA: {wa}\nLayanan: {jasa.upper()}\nDesign Pilihan: *{design_ref}*\n\n{detail_msg}\n\n📝 *CATATAN*: {ket_umum}"
        return redirect(f"https://wa.me/{nomor_admin}?text={urllib.parse.quote(pesan_wa)}")
    return render_template('order.html', referensi=referensi_pilihan)

if __name__ == '__main__':
    app.run(debug=True)