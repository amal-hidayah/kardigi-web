# Script untuk Menambahkan Contoh Artikel Blog

from app import app, db, BlogPost
from datetime import datetime

# Artikel contoh untuk testing
sample_posts = [
    {
        'title': '10 Tips Membuat Website Profesional untuk Bisnis UMKM',
        'content': '''
<h2>Mengapa Website Penting untuk Bisnis UMKM?</h2>
<p>Di era digital seperti sekarang, memiliki website profesional bukan lagi menjadi pilihan, melainkan <strong>kebutuhan</strong> bagi bisnis UMKM. Website menjadi wajah online bisnis Anda yang dapat diakses 24/7 oleh calon pelanggan dari mana saja.</p>

<h2>1. Pilih Domain yang Mudah Diingat</h2>
<p>Domain adalah alamat website Anda di internet. Pilih domain yang:</p>
<ul>
  <li>Singkat dan mudah diingat</li>
  <li>Mencerminkan nama bisnis Anda</li>
  <li>Gunakan ekstensi .com atau .id untuk bisnis lokal</li>
</ul>

<h2>2. Desain yang Responsif</h2>
<p>Pastikan website Anda <em>mobile-friendly</em> karena 60% pengunjung datang dari smartphone. Desain responsif akan membuat website tampil sempurna di semua perangkat.</p>

<h2>3. Konten yang Jelas dan Menarik</h2>
<p>Konten adalah raja! Pastikan:</p>
<ul>
  <li>Jelaskan produk/jasa dengan detail</li>
  <li>Gunakan gambar berkualitas tinggi</li>
  <li>Sertakan testimoni pelanggan</li>
  <li>Call-to-action yang jelas</li>
</ul>

<h2>4. Optimasi SEO dari Awal</h2>
<p>SEO (Search Engine Optimization) membantu website Anda muncul di hasil pencarian Google. Langkah-langkah dasar:</p>
<ol>
  <li>Riset keyword yang relevan</li>
  <li>Optimalkan meta title & description</li>
  <li>Gunakan heading dengan struktur yang benar</li>
  <li>Tambahkan alt text pada gambar</li>
</ol>

<h2>5. Kecepatan Loading yang Cepat</h2>
<p>Website yang lambat akan ditinggalkan pengunjung. Pastikan loading time di bawah 3 detik dengan cara:</p>
<ul>
  <li>Kompres gambar</li>
  <li>Gunakan hosting berkualitas</li>
  <li>Minimalkan penggunaan plugin berlebihan</li>
</ul>

<h2>Kesimpulan</h2>
<p>Membuat website profesional tidak harus mahal atau rumit. Dengan mengikuti 10 tips di atas, Anda bisa memiliki website yang menarik dan efektif untuk bisnis UMKM Anda.</p>

<p><strong>Butuh bantuan membuat website profesional?</strong> Konsultasikan dengan tim <a href="/">KARDIGI</a> sekarang juga!</p>
        ''',
        'excerpt': 'Pelajari 10 tips praktis membuat website profesional untuk bisnis UMKM Anda. Dari pemilihan domain hingga optimasi SEO.',
        'meta_description': 'Panduan lengkap membuat website profesional untuk bisnis UMKM. Tips praktis dari domain, desain, hingga SEO. Konsultasi gratis!',
        'meta_keywords': 'website umkm, jasa website, pembuatan website, website bisnis, tips website, website murah',
        'published': True
    },
    {
        'title': 'Cara Membuat CV ATS-Friendly yang Lolos Seleksi',
        'content': '''
<h2>Apa Itu ATS?</h2>
<p><strong>ATS (Applicant Tracking System)</strong> adalah sistem yang digunakan perusahaan untuk menyaring CV secara otomatis. Lebih dari 75% perusahaan besar menggunakan ATS untuk efisiensi rekrutmen.</p>

<h2>Mengapa CV Anda Harus ATS-Friendly?</h2>
<p>Meskipun Anda kandidat yang qualified, CV yang tidak ATS-friendly bisa langsung ter-reject oleh sistem sebelum dilihat HRD. Oleh karena itu, penting untuk membuat CV yang bisa <em>dibaca</em> oleh sistem ATS.</p>

<h2>Tips Membuat CV ATS-Friendly</h2>

<h3>1. Gunakan Format Sederhana</h3>
<ul>
  <li>Hindari desain yang terlalu kompleks</li>
  <li>Gunakan font standar (Arial, Calibri, Times New Roman)</li>
  <li>Jangan gunakan tabel atau kolom</li>
  <li>Simpan dalam format .docx atau PDF</li>
</ul>

<h3>2. Gunakan Keyword yang Tepat</h3>
<p>ATS akan mencari keyword yang sesuai dengan job description. Cara menentukan keyword:</p>
<ol>
  <li>Baca job description dengan teliti</li>
  <li>Catat skill dan kualifikasi yang disebutkan</li>
  <li>Masukkan keyword tersebut di CV Anda secara natural</li>
  <li>Gunakan istilah yang sama persis (contoh: "Digital Marketing" bukan "Pemasaran Digital")</li>
</ol>

<h3>3. Struktur CV yang Jelas</h3>
<p>Gunakan heading standar yang mudah dibaca ATS:</p>
<ul>
  <li><strong>Data Diri / Contact Information</strong></li>
  <li><strong>Ringkasan Profesional / Professional Summary</strong></li>
  <li><strong>Pengalaman Kerja / Work Experience</strong></li>
  <li><strong>Pendidikan / Education</strong></li>
  <li><strong>Keahlian / Skills</strong></li>
  <li><strong>Sertifikasi / Certifications</strong> (jika ada)</li>
</ul>

<h3>4. Hindari Elemen Visual Berlebihan</h3>
<p>ATS sulit membaca:</p>
<ul>
  <li>Gambar dan foto</li>
  <li>Grafik dan chart</li>
  <li>Header dan footer yang kompleks</li>
  <li>Text box</li>
</ul>

<h3>5. Sesuaikan CV untuk Setiap Lamaran</h3>
<p>Jangan kirim CV yang sama untuk semua posisi. Sesuaikan keyword dan pengalaman yang relevan dengan posisi yang dilamar.</p>

<h2>Contoh Template CV ATS-Friendly</h2>
<p>Struktur dasar CV yang ATS-friendly:</p>
<ol>
  <li>Nama dan Kontak di atas</li>
  <li>Professional Summary (2-3 kalimat)</li>
  <li>Pengalaman Kerja (reverse chronological)</li>
  <li>Pendidikan</li>
  <li>Skills (bullet points)</li>
  <li>Sertifikasi dan Achievement</li>
</ol>

<h2>Kesimpulan</h2>
<p>CV ATS-friendly meningkatkan peluang Anda lolos seleksi administrasi hingga 60%. Fokus pada kesederhanaan, keyword yang tepat, dan struktur yang jelas.</p>

<p><strong>Butuh bantuan membuat CV ATS-friendly?</strong> Gunakan layanan <a href="/jasa-cv">Jasa CV KARDIGI</a> dengan harga terjangkau mulai Rp20.000!</p>
        ''',
        'excerpt': 'Panduan lengkap membuat CV ATS-Friendly agar lolos seleksi administrasi. Tips praktis yang terbukti efektif meningkatkan peluang diterima kerja.',
        'meta_description': 'Cara membuat CV ATS-Friendly yang lolos seleksi. Panduan lengkap dari format, keyword, hingga struktur CV yang tepat. Tingkatkan peluang diterima!',
        'meta_keywords': 'cv ats, cv ats friendly, cara membuat cv, jasa cv, cv profesional, tips cv, cv lolos seleksi',
        'published': True
    },
    {
        'title': '5 Kesalahan Fatal dalam Membangun Website yang Harus Dihindari',
        'content': '''
<h2>Pendahuluan</h2>
<p>Membangun website adalah investasi penting untuk bisnis digital Anda. Namun, banyak pemilik bisnis yang melakukan kesalahan fatal yang membuat website tidak efektif. Mari kita bahas 5 kesalahan paling umum dan cara menghindarinya.</p>

<h2>1. Tidak Memikirkan User Experience (UX)</h2>
<p>Kesalahan terbesar adalah membuat website tanpa memikirkan pengalaman pengguna. Website yang sulit dinavigasi akan membuat pengunjung pergi.</p>

<h3>Dampaknya:</h3>
<ul>
  <li>Bounce rate tinggi (pengunjung langsung keluar)</li>
  <li>Conversion rate rendah</li>
  <li>Reputasi buruk</li>
</ul>

<h3>Solusinya:</h3>
<ul>
  <li>Buat navigasi yang intuitif</li>
  <li>Gunakan call-to-action yang jelas</li>
  <li>Test website dengan user real</li>
  <li>Pastikan loading time cepat</li>
</ul>

<h2>2. Mengabaikan Mobile Optimization</h2>
<p>Lebih dari 60% traffic datang dari mobile. Website yang tidak mobile-friendly akan kehilangan banyak potential customers.</p>

<h3>Ciri-ciri website tidak mobile-friendly:</h3>
<ol>
  <li>Text terlalu kecil untuk dibaca</li>
  <li>Button terlalu kecil untuk diklik</li>
  <li>Konten tidak muat di layar</li>
  <li>Loading sangat lambat di mobile</li>
</ol>

<h3>Solusinya:</h3>
<p>Gunakan <strong>responsive design</strong> yang otomatis menyesuaikan tampilan dengan ukuran layar. Test di berbagai device sebelum launch.</p>

<h2>3. Konten yang Tidak Jelas</h2>
<p>Banyak website yang gagal karena tidak jelas menawarkan apa. Pengunjung harus langsung tahu:</p>
<ul>
  <li>Apa yang Anda tawarkan</li>
  <li>Mengapa mereka harus memilih Anda</li>
  <li>Apa yang harus mereka lakukan selanjutnya</li>
</ul>

<h3>Solusinya:</h3>
<ol>
  <li>Buat headline yang powerful di homepage</li>
  <li>Jelaskan value proposition dengan jelas</li>
  <li>Sertakan call-to-action yang spesifik</li>
  <li>Gunakan visual yang mendukung pesan</li>
</ol>

<h2>4. Tidak Mengoptimalkan SEO</h2>
<p>Website yang indah tapi tidak terindex Google = <em>tidak ada gunanya</em>. SEO harus dipikirkan dari awal.</p>

<h3>Kesalahan SEO yang sering terjadi:</h3>
<ul>
  <li>Tidak ada keyword research</li>
  <li>Meta description kosong</li>
  <li>Gambar tanpa alt text</li>
  <li>URL tidak SEO-friendly</li>
  <li>Loading time lambat</li>
</ul>

<h3>Solusinya:</h3>
<p>Lakukan SEO on-page dari awal: riset keyword, optimasi meta tags, struktur heading yang benar, dan internal linking yang baik.</p>

<h2>5. Tidak Ada Sistem Maintenance</h2>
<p>Website bukan "buat sekali jadi selamanya". Website perlu di-maintain secara berkala untuk:</p>
<ul>
  <li>Update keamanan</li>
  <li>Fix bugs</li>
  <li>Update konten</li>
  <li>Monitor performance</li>
</ul>

<h3>Solusinya:</h3>
<p>Buat jadwal maintenance rutin minimal sebulan sekali. Atau gunakan jasa maintenance profesional.</p>

<h2>Kesimpulan</h2>
<p>Menghindari 5 kesalahan fatal ini akan membuat website Anda lebih efektif dan menghasilkan ROI yang lebih baik. Ingat: website adalah investasi jangka panjang untuk bisnis Anda.</p>

<p><strong>Ingin website profesional yang bebas dari kesalahan-kesalahan di atas?</strong> Hubungi <a href="/">KARDIGI</a> untuk konsultasi gratis!</p>
        ''',
        'excerpt': '5 kesalahan fatal yang sering terjadi dalam pembuatan website dan cara menghindarinya. Pelajari agar website Anda efektif dan menghasilkan.',
        'meta_description': 'Hindari 5 kesalahan fatal dalam membangun website. Dari UX, mobile optimization, hingga SEO. Panduan lengkap untuk website yang efektif.',
        'meta_keywords': 'kesalahan website, tips website, pembuatan website, website profesional, web design, website efektif',
        'published': True
    }
]

def add_sample_posts():
    with app.app_context():
        # Check if posts already exist
        existing = BlogPost.query.count()
        if existing > 0:
            print(f"Database sudah memiliki {existing} artikel. Skip inserting sample data.")
            return
        
        print("Menambahkan artikel contoh...")
        for post_data in sample_posts:
            # Generate slug
            slug = post_data['title'].lower()
            slug = slug.replace(' ', '-')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')
            
            post = BlogPost(
                title=post_data['title'],
                slug=slug,
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                meta_description=post_data['meta_description'],
                meta_keywords=post_data['meta_keywords'],
                published=post_data['published']
            )
            db.session.add(post)
            print(f"✓ Menambahkan: {post_data['title']}")
        
        db.session.commit()
        print(f"\n✅ Berhasil menambahkan {len(sample_posts)} artikel contoh!")
        print("Akses /blog untuk melihat hasilnya.")

if __name__ == '__main__':
    add_sample_posts()
