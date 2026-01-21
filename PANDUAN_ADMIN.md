# 📋 PANDUAN UPLOAD PORTFOLIO - KARDIGI Admin

## 🎯 Portfolio Website & CV Sudah KOSONG
Database portfolio telah di-reset. Admin bisa mulai upload portfolio baru dari panel admin.

---

## 🔐 Login Admin
1. Buka: `https://kardigi.tech/login`
2. Username: `admin`
3. Password: `kardigi123`

---

## 📤 Upload Portfolio Website

### Langkah-Langkah:
1. Login ke `/admin`
2. Isi form upload:
   - **Kategori:** Pilih jenis website (Company Profile / Toko Online / dll)
   - **Judul Project:** Contoh: "Toko Elektronik Sukabumi"
   - **Deskripsi:** Fitur unggulan website
   - **Thumbnail:** Upload gambar preview (JPG/PNG, max 1200px width)
   - **File ZIP:** Upload website lengkap (wajib ada `index.html`)
3. Klik "Upload Referensi"

### ✅ Hasil:
- Thumbnail otomatis dioptimasi (max 1200px, quality 75%)
- ZIP otomatis di-ekstrak ke `static/demos/<nama-folder>/`
- Website langsung bisa di-preview di `/demo/<nama-folder>/`
- Otomatis muncul di landing page `/jasa-website` dengan button "Lihat Live Demo"

---

## 📄 Upload Portfolio CV

### Langkah-Langkah:
1. Login ke `/admin`
2. Isi form upload:
   - **Kategori:** Pilih jenis CV (CV ATS / CV Kreatif / Surat Lamaran)
   - **Judul Project:** Contoh: "CV ATS Fresh Graduate"
   - **Deskripsi:** Keunggulan template CV
   - **Thumbnail:** Upload preview CV (JPG/PNG)
   - **File Project:** Upload CV final (PDF/JPG/PNG)
3. Klik "Upload Referensi"

### ✅ Hasil:
- File CV tersimpan di `static/files_cv/`
- Otomatis muncul di landing page `/jasa-cv`

---

## 🎨 Tips Upload Portfolio:

### Website:
- **Struktur ZIP:**
  ```
  website-name.zip
  ├── index.html      (wajib ada!)
  ├── style.css
  ├── script.js
  └── img/
      └── logo.png
  ```
- Pastikan semua link gambar & CSS menggunakan **relative path**
- Test dulu di lokal sebelum upload
- Ukuran thumbnail: 500x300px (landscape)

### CV:
- Format thumbnail: 600x850px (portrait)
- File CV: PDF (max 5MB) atau JPG/PNG
- Gunakan nama file yang jelas, contoh: `cv-ats-professional.pdf`

---

## 📊 Dashboard Admin

### Fitur:
- **Lihat semua upload:** Table dengan thumbnail, judul, kategori
- **Preview live demo:** Button "Demo" untuk website
- **Hapus portfolio:** Button delete dengan konfirmasi

### Portfolio yang Muncul di Landing Page:
- `/jasa-website` → 6 portfolio website terbaru
- `/jasa-cv` → 6 portfolio CV terbaru
- Urutkan otomatis: terbaru di atas

---

## 🚀 Deployment Checklist

Setelah upload portfolio:
1. ✅ Test live demo: `/demo/<folder-name>/`
2. ✅ Cek landing page: `/jasa-website` dan `/jasa-cv`
3. ✅ Pastikan thumbnail loading cepat
4. ✅ Submit ulang sitemap ke Google Search Console

---

## 🆘 Troubleshooting

**❌ Demo website tidak muncul:**
- Pastikan ZIP punya `index.html` di root
- Cek folder `static/demos/` apakah ter-ekstrak dengan benar

**❌ Thumbnail tidak muncul:**
- Pastikan format JPG/PNG
- Cek folder `static/uploads/`

**❌ Portfolio tidak muncul di landing page:**
- Refresh browser (Ctrl + F5)
- Cek database: apakah kategori sudah benar ('website' atau 'cv')

---

## 📞 Support
Masalah teknis? Chat: **+62 895-0995-1772** (WhatsApp)
