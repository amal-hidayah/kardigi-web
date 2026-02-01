import os
import zipfile
import shutil
import urllib.parse
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from functools import wraps
from PIL import Image
from datetime import datetime

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

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEMO_FOLDER'] = DEMO_FOLDER

# Pastikan folder tersedia otomatis
for folder in [UPLOAD_FOLDER, DEMO_FOLDER]:
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

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    image = db.Column(db.String(200))
    meta_title = db.Column(db.String(60))
    meta_description = db.Column(db.String(160))
    meta_keywords = db.Column(db.String(255))
    focus_keyword = db.Column(db.String(100))
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

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
def home(): 
    # Ambil 3 artikel blog terbaru yang sudah dipublish
    latest_posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('index.html', latest_posts=latest_posts)

@app.route('/jasa-website')
def jasa_website(): 
    portfolio_website = PortfolioWebsite.query.order_by(PortfolioWebsite.id.desc()).all()
    return render_template('jasa_website.html', portfolio=portfolio_website)

# --- BLOG ROUTES ---
@app.route('/blog')
def blog_list():
    """Halaman daftar artikel blog"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('blog_list.html', posts=posts)

@app.route('/blog/<slug>')
def blog_detail(slug):
    """Halaman detail artikel blog dengan SEO optimization"""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    # Get related posts (latest 3 posts excluding current)
    related_posts = BlogPost.query.filter(BlogPost.id != post.id, BlogPost.published == True).order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('blog_detail.html', post=post, related_posts=related_posts)

def create_slug(title):
    """Generate SEO-friendly slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = slug.strip('-')
    # Check if slug exists, add number if duplicate
    original_slug = slug
    counter = 1
    while BlogPost.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1
    return slug

@app.route('/admin/blog/new', methods=['GET', 'POST'])
@login_required
def new_blog_post():
    """Halaman tambah artikel blog baru"""
    if request.method == 'GET':
        return render_template('admin_blog_form.html', mode='new')
    
    try:
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt', '')
        meta_title = request.form.get('meta_title', '')
        meta_description = request.form.get('meta_description', '')
        meta_keywords = request.form.get('meta_keywords', '')
        focus_keyword = request.form.get('focus_keyword', '')
        published = request.form.get('published') == 'on'
        
        # Ambil slug dari form jika diisi, jika tidak generate dari judul
        form_slug = request.form.get('slug', '').strip()
        if form_slug:
            # Normalisasi slug: huruf kecil, hanya a-z, 0-9, -
            slug = re.sub(r'[^a-z0-9-]', '', form_slug.lower())
            # Pastikan slug unik
            original_slug = slug
            counter = 1
            while BlogPost.query.filter_by(slug=slug).first():
                slug = f"{original_slug}-{counter}"
                counter += 1
        else:
            slug = create_slug(title)
        
        # Handle image upload
        image_filename = None
        file_img = request.files.get('image')
        if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
            filename_img = secure_filename(file_img.filename)
            # Add timestamp to avoid conflicts
            filename_img = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename_img}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_img)
            
            # Optimize image
            img = Image.open(file_img)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img.save(filepath, 'JPEG', quality=85, optimize=True)
            image_filename = filename_img
        
        # Create new post with backward compatibility
        try:
            new_post = BlogPost(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                image=image_filename,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                focus_keyword=focus_keyword,
                published=published
            )
        except TypeError:
            # Fallback if meta_title or focus_keyword columns don't exist yet
            new_post = BlogPost(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                image=image_filename,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                published=published
            )
        
        db.session.add(new_post)
        db.session.commit()
        flash(f"Artikel '{title}' berhasil ditambahkan!", "success")
        return redirect(url_for('admin_page') + '#blog')
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('admin_page') + '#blog')

@app.route('/admin/blog/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(id):
    """Halaman edit artikel blog"""
    post = BlogPost.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('admin_blog_form.html', mode='edit', post=post)
    
    try:
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.excerpt = request.form.get('excerpt', '')
        
        # Safely set new fields if they exist in database
        try:
            post.meta_title = request.form.get('meta_title', '')
            post.focus_keyword = request.form.get('focus_keyword', '')
        except AttributeError:
            # Columns don't exist yet, skip them
            pass
        
        post.meta_description = request.form.get('meta_description', '')
        post.meta_keywords = request.form.get('meta_keywords', '')
        post.published = request.form.get('published') == 'on'
        
        # Update slug jika diisi di form, jika tidak tetap/auto dari judul
        form_slug = request.form.get('slug', '').strip()
        if form_slug:
            new_slug = re.sub(r'[^a-z0-9-]', '', form_slug.lower())
            # Pastikan slug unik (kecuali milik post ini sendiri)
            existing = BlogPost.query.filter(BlogPost.slug == new_slug, BlogPost.id != post.id).first()
            if not existing:
                post.slug = new_slug
        else:
            # Jika slug kosong, update slug dari judul jika berubah
            new_slug = create_slug(post.title)
            if new_slug != post.slug:
                existing = BlogPost.query.filter(BlogPost.slug == new_slug, BlogPost.id != post.id).first()
                if not existing:
                    post.slug = new_slug
        
        # Handle new image upload
        file_img = request.files.get('image')
        if file_img and allowed_file(file_img.filename, ALLOWED_EXTENSIONS_IMG):
            # Delete old image if exists
            if post.image:
                try:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.image))
                except:
                    pass
            
            filename_img = secure_filename(file_img.filename)
            filename_img = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename_img}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename_img)
            
            # Optimize image
            img = Image.open(file_img)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img.save(filepath, 'JPEG', quality=85, optimize=True)
            post.image = filename_img
        
        db.session.commit()
        flash(f"Artikel '{post.title}' berhasil diupdate!", "success")
        return redirect(url_for('admin_page') + '#blog')
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating article: {str(e)}", "danger")
        return redirect(url_for('admin_page') + '#blog')

@app.route('/admin/blog/delete/<int:id>')
@login_required
def delete_blog_post(id):
    """Hapus artikel blog"""
    post = BlogPost.query.get_or_404(id)
    
    # Delete image if exists
    if post.image:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], post.image))
        except:
            pass
    
    db.session.delete(post)
    db.session.commit()
    flash("Artikel berhasil dihapus!", "success")
    return redirect(url_for('admin_page') + '#blog')

# --- REDIRECTS (untuk backward compatibility) ---
@app.route('/katalog')
def katalog_home(): return redirect(url_for('home'))

@app.route('/katalog/website')
def katalog_website(): return redirect(url_for('jasa_website'))

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
    blog_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin.html', 
                         pesanan=pesanan, 
                         portfolio_websites=portfolio_websites,
                         blog_posts=blog_posts)

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
    """Generate dynamic sitemap including blog posts"""
    from flask import make_response
    
    # Static pages
    pages = [
        {'loc': url_for('home', _external=True), 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': url_for('jasa_website', _external=True), 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': url_for('blog_list', _external=True), 'changefreq': 'daily', 'priority': '0.9'},
    ]
    
    # Add blog posts
    blog_posts = BlogPost.query.filter_by(published=True).all()
    for post in blog_posts:
        pages.append({
            'loc': url_for('blog_detail', slug=post.slug, _external=True),
            'lastmod': post.updated_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.8'
        })
    
    # Generate XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for page in pages:
        xml += '  <url>\n'
        xml += f'    <loc>{page["loc"]}</loc>\n'
        if 'lastmod' in page:
            xml += f'    <lastmod>{page["lastmod"]}</lastmod>\n'
        xml += f'    <changefreq>{page["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{page["priority"]}</priority>\n'
        xml += '  </url>\n'
    
    xml += '</urlset>'
    
    response = make_response(xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)