# 🔍 Panduan Setup Google Search Console - KARDIGI

## Step 1: Verify Website Ownership

### A. Login ke Google Search Console
1. Buka: https://search.google.com/search-console/
2. Login dengan akun Google kamu
3. Klik **"Add Property"** / **"Tambahkan Properti"**

### B. Pilih Tipe Property
Pilih **"URL prefix"** (bukan Domain):
```
https://kardigi.tech
```
*Catatan: Gunakan URL lengkap dengan https://*

### C. Verify Ownership - Pilih Metode

#### **Metode 1: HTML Meta Tag (RECOMMENDED - Paling Mudah)**

1. Google akan kasih meta tag seperti ini:
```html
<meta name="google-site-verification" content="ABC123XYZ..." />
```

2. Copy meta tag tersebut

3. Buka file `templates/base.html` di project

4. Tambahkan meta tag di dalam `<head>`, setelah charset:
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Google Search Console Verification -->
    <meta name="google-site-verification" content="ABC123XYZ..." />
    
    <!-- SEO Meta Tags -->
    ...
```

5. Commit dan push ke GitHub:
```bash
git add templates/base.html
git commit -m "Add Google Search Console verification"
git push origin main
```

6. Deploy ke production:
```bash
# Di SSH terminal
cd ~/kardigi-web
git pull origin main
sudo systemctl restart kardigi
```

7. Kembali ke Google Search Console, klik **"Verify"**

✅ **Done!** Website terverifikasi.

---

#### **Metode 2: HTML File Upload (Alternative)**

1. Google akan suruh download file: `google[...].html`
2. Upload file ke folder `static/` di project
3. File akan accessible di: `https://kardigi.tech/static/google[...].html`
4. Klik **"Verify"** di Google Search Console

---

## Step 2: Submit Sitemap

Setelah verified, submit sitemap agar Google crawl semua halaman:

1. Di Google Search Console, sidebar kiri → **"Sitemaps"**
2. Di kolom **"Add a new sitemap"**, masukkan:
```
https://kardigi.tech/sitemap.xml
```
3. Klik **"Submit"**

✅ Google akan mulai crawl website kamu!

**Status yang akan muncul:**
- **Success**: Sitemap diterima
- **Discovered**: Google menemukan URL
- **Indexed**: URL sudah masuk Google Search

---

## Step 3: Request Indexing (Opsional tapi Recommended)

Untuk indexing lebih cepat:

### A. Homepage
1. Di Search Console, klik **"URL Inspection"** (sidebar kiri)
2. Paste URL: `https://kardigi.tech`
3. Klik **"Request Indexing"**
4. Tunggu proses (5-10 detik)

### B. Service Page
1. URL Inspection → `https://kardigi.tech/jasa-website`
2. Request Indexing

### C. Blog Posts (saat sudah ada artikel)
1. URL Inspection → `https://kardigi.tech/blog/judul-artikel`
2. Request Indexing

**Catatan:** Google punya limit harian (~10 request/hari), jadi prioritaskan halaman penting dulu.

---

## Step 4: Monitor Performance

### Dashboard Overview
Setelah 2-3 hari, kamu bisa lihat:
- **Impressions**: Berapa kali website muncul di Google
- **Clicks**: Berapa kali orang klik website
- **CTR**: Click-through rate (%)
- **Position**: Ranking rata-rata

### Performance Report
1. Sidebar → **"Performance"**
2. Lihat query apa yang membawa traffic
3. Halaman mana yang paling populer

### Coverage Report
1. Sidebar → **"Coverage"**
2. Lihat halaman mana yang sudah indexed
3. Fix error kalau ada (404, server error, dll)

---

## Step 5: Check Rich Results

Test structured data (Schema.org):

1. Buka: https://search.google.com/test/rich-results
2. Masukkan URL: `https://kardigi.tech`
3. Klik **"Test URL"**

**Expected Results:**
- ✅ LocalBusiness schema detected
- ✅ Valid structured data

Untuk blog post:
1. Test URL: `https://kardigi.tech/blog/judul-artikel`
2. Should detect: **BlogPosting** schema

---

## Timeline & Expectations

### Day 1-2: Verification & Submission
- ✅ Verify ownership
- ✅ Submit sitemap
- ⏳ Google mulai crawl (1-24 jam)

### Day 3-7: Initial Indexing
- 📊 Data mulai muncul di Performance report
- 📈 Halaman utama mulai indexed
- 🔍 Website mulai muncul di search (terbatas)

### Week 2-4: Growing Visibility
- 🚀 Lebih banyak halaman indexed
- 📈 Ranking mulai naik untuk keyword tertentu
- 💡 Lihat query yang membawa traffic

### Month 2-3: Established Presence
- 💪 Ranking stabil/naik
- 📊 Traffic organik mulai signifikan
- 🎯 Optimize based on GSC data

---

## Troubleshooting Common Issues

### ❌ "Verification Failed"
**Penyebab:**
- Meta tag salah tempat
- File verification tidak accessible
- Website down saat verification

**Solusi:**
1. Cek meta tag ada di `<head>` section
2. Test access: https://kardigi.tech (harus load)
3. Clear cache browser, coba lagi

### ⚠️ "Sitemap couldn't be read"
**Penyebab:**
- Sitemap tidak accessible
- Format XML error
- Server down

**Solusi:**
1. Test sitemap: https://kardigi.tech/sitemap.xml (harus bisa dibuka)
2. Validate XML: https://www.xmlvalidation.com/
3. Check server logs: `sudo journalctl -u kardigi`

### 🐌 "Discovered but not indexed"
**Penyebab:**
- Google belum sempat index
- Content quality rendah
- Duplicate content

**Solusi:**
1. Tunggu 1-2 minggu
2. Request indexing manual (URL Inspection)
3. Improve content quality

### 📉 "Valid but with warnings"
**Penyebab:**
- Schema.org incomplete
- Missing recommended fields

**Solusi:**
1. Check Rich Results Test
2. Add missing schema fields
3. Re-submit untuk re-crawl

---

## Best Practices

### ✅ DO:
1. **Submit sitemap** setelah verify
2. **Request indexing** untuk halaman penting
3. **Monitor weekly** untuk errors
4. **Add new blog posts** to sitemap (auto-generated)
5. **Check mobile usability**
6. **Fix crawl errors** immediately

### ❌ DON'T:
1. **Jangan request indexing** terlalu sering (max 10/day)
2. **Jangan ignore** crawl errors
3. **Jangan duplicate** content
4. **Jangan keyword stuffing**
5. **Jangan cloaking** (different content for Google vs users)

---

## Maintenance Checklist

### Daily:
- [ ] Check for critical errors (jika ada notif)

### Weekly:
- [ ] Check Performance report
- [ ] Monitor impressions & clicks
- [ ] Check for new crawl errors

### Monthly:
- [ ] Review top queries
- [ ] Optimize low-performing pages
- [ ] Update sitemap (auto for blog posts)
- [ ] Check Core Web Vitals

### After Publishing Blog Post:
- [ ] Auto-included in sitemap (dynamic)
- [ ] Request indexing via URL Inspection
- [ ] Share on social media (for backlinks)

---

## Expected Results for KARDIGI

### Target Keywords:
1. **"jasa website sukabumi"** → Homepage
2. **"jasa pembuatan website sukabumi"** → Homepage
3. **"web developer sukabumi"** → Homepage
4. **"jasa website murah sukabumi"** → Jasa Website page
5. **Blog keywords** → Individual articles

### Realistic Timeline:
- **Week 1**: 0-10 impressions/day
- **Week 2**: 10-50 impressions/day
- **Month 1**: 50-200 impressions/day
- **Month 3**: 200-500 impressions/day
- **Month 6**: 500-1000+ impressions/day

*Note: Actual results depend on content quality, backlinks, and competition*

---

## Contact & Support

**Website:** https://kardigi.tech  
**Email:** kardigi.id@gmail.com  
**WhatsApp:** +6289509951772

**Useful Links:**
- Google Search Console: https://search.google.com/search-console/
- Rich Results Test: https://search.google.com/test/rich-results
- Mobile-Friendly Test: https://search.google.com/test/mobile-friendly
- PageSpeed Insights: https://pagespeed.web.dev/

---

**Last Updated:** February 1, 2026  
**Status:** Ready for Google Search Console setup ✅
