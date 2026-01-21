import os
import zipfile
import shutil
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
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

class PortfolioWebsite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200), nullable=False)
    demo_link = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.now())

class PortfolioCV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

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

@app.route('/jasa-website')
def jasa_website(): 
    portfolio_website = PortfolioWebsite.query.order_by(PortfolioWebsite.id.desc()).all()
    return render_template('jasa_website.html', portfolio=portfolio_website)

@app.route('/jasa-cv')
def jasa_cv(): 
    portfolio_cv = PortfolioCV.query.order_by(PortfolioCV.id.desc()).all()
    return render_template('jasa_cv.html', portfolio=portfolio_cv)

@app.route('/generator')
def cv_generator():
    return render_template('generator_cv.html')

# --- REDIRECTS (untuk backward compatibility) ---
@app.route('/katalog')
def katalog_home(): return redirect(url_for('home'))

@app.route('/katalog/website')
def katalog_website(): return redirect(url_for('jasa_website'))

@app.route('/katalog/cv')
def katalog_cv_redirect(): return redirect(url_for('jasa_cv'))

@app.route('/order')
def order_redirect(): return redirect(url_for('jasa_website'))

@app.route('/referensi/<id_layanan>')
def showcase_redirect(id_layanan): return redirect(url_for('jasa_website'))

# --- ROUTE ADMIN ---
@app.route('/admin')
@login_required
def admin_page():
    pesanan = Order.query.order_by(Order.id.desc()).all()
    portfolio_websites = PortfolioWebsite.query.order_by(PortfolioWebsite.id.desc()).all()
    portfolio_cvs = PortfolioCV.query.order_by(PortfolioCV.id.desc()).all()
    return render_template('admin.html', 
                         pesanan=pesanan, 
                         portfolio_websites=portfolio_websites,
                         portfolio_cvs=portfolio_cvs)

@app.route('/hapus_order/<int:id>')
@login_required
def hapus_pesanan(id):
    item = Order.query.get(id); db.session.delete(item); db.session.commit()
    return redirect(url_for('admin_page'))

# --- PORTFOLIO WEBSITE ROUTES ---
@app.route('/admin/upload_portfolio_website', methods=['POST'])
@login_required
def upload_portfolio_website():
    title = request.form.get('title')
    description = request.form.get('description', '')
    demo_link = request.form.get('demo_link', '')
    
    file_img = request.files.get('image')
    if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
        filename_img = secure_filename(file_img.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_img)
        
        # Optimize image
        img = Image.open(file_img)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        
        new_portfolio = PortfolioWebsite(title=title, description=description, image=filename_img, demo_link=demo_link)
        db.session.add(new_portfolio)
        db.session.commit()
        flash("Portfolio Website berhasil ditambahkan!", "success")
    else:
        flash("Gagal upload gambar!", "danger")
    
    return redirect(url_for('admin_page'))

@app.route('/admin/delete_portfolio_website/<int:id>')
@login_required
def delete_portfolio_website(id):
    item = PortfolioWebsite.query.get(id)
    if item:
        try: 
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.image))
        except: 
            pass
        db.session.delete(item)
        db.session.commit()
        flash("Portfolio Website dihapus.", "success")
    return redirect(url_for('admin_page'))

# --- PORTFOLIO CV ROUTES ---
@app.route('/admin/upload_portfolio_cv', methods=['POST'])
@login_required
def upload_portfolio_cv():
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    file_img = request.files.get('image')
    if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
        filename_img = secure_filename(file_img.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_img)
        
        # Optimize image
        img = Image.open(file_img)
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        
        new_portfolio = PortfolioCV(title=title, description=description, image=filename_img)
        db.session.add(new_portfolio)
        db.session.commit()
        flash("Portfolio CV berhasil ditambahkan!", "success")
    else:
        flash("Gagal upload gambar!", "danger")
    
    return redirect(url_for('admin_page'))

@app.route('/admin/delete_portfolio_cv/<int:id>')
@login_required
def delete_portfolio_cv(id):
    item = PortfolioCV.query.get(id)
    if item:
        try: 
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.image))
        except: 
            pass
        db.session.delete(item)
        db.session.commit()
        flash("Portfolio CV dihapus.", "success")
    return redirect(url_for('admin_page'))

# --- ROUTE LIVE DEMO WEBSITE ---
@app.route('/demo/<folder_name>/')
@app.route('/demo/<folder_name>/<path:filename>')
def serve_demo(folder_name, filename='index.html'):
    """Serve live demo website yang diupload admin"""
    demo_path = os.path.join(app.config['DEMO_FOLDER'], folder_name)
    if not os.path.exists(demo_path):
        flash("Demo tidak ditemukan!", "warning")
        return redirect(url_for('home'))
    return send_from_directory(demo_path, filename)

# --- ROUTE SEO: ROBOTS.TXT & SITEMAP.XML ---
@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml', mimetype='application/xml')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)