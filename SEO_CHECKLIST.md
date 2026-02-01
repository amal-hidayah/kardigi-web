# 📊 KARDIGI SEO & Google Search Console Setup Guide

## ✅ SEO Checklist - Status

### 1. **Meta Tags** ✅
- ✅ Title tags (optimal 50-60 characters)
- ✅ Meta descriptions (optimal 150-160 characters)
- ✅ Meta keywords
- ✅ Canonical URLs
- ✅ Robots meta (index, follow)

### 2. **Open Graph (Facebook/LinkedIn Share)** ✅
- ✅ og:title, og:description, og:type
- ✅ og:image (using logo.png as fallback)
- ✅ og:image:width, og:image:height, og:image:alt
- ✅ og:url, og:site_name, og:locale
- ✅ Article metadata for blog posts

### 3. **Twitter Cards** ✅
- ✅ twitter:card (summary_large_image)
- ✅ twitter:title, twitter:description
- ✅ twitter:image, twitter:image:alt

### 4. **Structured Data (Schema.org)** ✅
- ✅ LocalBusiness schema (base.html)
- ✅ BlogPosting schema (blog_detail.html)
- ✅ BreadcrumbList schema (blog pages)

### 5. **Sitemap & Robots** ✅
- ✅ Dynamic sitemap: `/sitemap.xml` (auto-generated with blog posts)
- ✅ Static sitemap: `/static/sitemap.xml` (backup)
- ✅ robots.txt configured properly
- ✅ Disallow admin and login pages

### 6. **Favicon** ✅
- ✅ favicon.png (32x32, 16x16)
- ✅ Apple touch icon (180x180)
- ✅ Theme color meta tag
- ✅ Multiple format support

### 7. **Blog SEO Features** ✅
- ✅ Focus keyword tracking
- ✅ Meta title (60 chars max)
- ✅ Meta description (160 chars max)
- ✅ Auto-generated slugs (SEO-friendly URLs)
- ✅ Google Search Preview
- ✅ Word counter
- ✅ Keyword density checker

---

## 🚀 Google Search Console Setup

### Step 1: Verify Website Ownership

**Method A: HTML File Upload (Recommended)**
1. Login ke [Google Search Console](https://search.google.com/search-console/)
2. Klik "Add Property" → Pilih "URL prefix" → Masukkan `https://kardigi.tech`
3. Pilih verification method: "HTML file"
4. Download file `google[...].html`
5. Upload ke folder `static/` di project
6. Klik "Verify"

**Method B: HTML Meta Tag**
1. Google akan kasih meta tag seperti: `<meta name="google-site-verification" content="[CODE]" />`
2. Tambahkan di `templates/base.html` di dalam `<head>`
3. Deploy website
4. Klik "Verify" di Google Search Console

### Step 2: Submit Sitemap
1. Di Google Search Console, pilih property Anda
2. Sidebar kiri → "Sitemaps"
3. Masukkan URL sitemap: `https://kardigi.tech/sitemap.xml`
4. Klik "Submit"

### Step 3: Request Indexing
Untuk setiap blog post baru:
1. Go to "URL Inspection" di sidebar
2. Paste URL blog post (contoh: `https://kardigi.tech/blog/tips-membuat-website`)
3. Klik "Request Indexing"
4. Google akan crawl dalam 1-7 hari

---

## 🔍 SEO Testing Tools

### Check Your Website:
1. **Google Rich Results Test**: https://search.google.com/test/rich-results
   - Test structured data (schema.org)
   
2. **Facebook Sharing Debugger**: https://developers.facebook.com/tools/debug/
   - Test Open Graph tags
   - Clear Facebook cache
   
3. **Twitter Card Validator**: https://cards-dev.twitter.com/validator
   - Test Twitter Card preview
   
4. **Google PageSpeed Insights**: https://pagespeed.web.dev/
   - Test performance & SEO score
   
5. **Mobile-Friendly Test**: https://search.google.com/test/mobile-friendly
   - Test responsive design

---

## 📝 Blog SEO Best Practices

### When Creating New Blog Post:

1. **Judul (Title)**
   - 50-60 karakter optimal
   - Include focus keyword di awal
   - Buat menarik & clickable

2. **Meta Description**
   - 150-160 karakter optimal
   - Include focus keyword
   - Action-oriented (ajakan)
   - Jelaskan value proposition

3. **Focus Keyword**
   - Pilih 1 keyword utama
   - Pastikan muncul di:
     - Judul (H1)
     - Meta description
     - Konten (2-3% density)
     - URL slug

4. **Content Structure**
   - Minimal 800-1500 kata untuk artikel SEO
   - Gunakan heading (H2, H3) untuk struktur
   - Paragraf pendek (2-4 kalimat)
   - Bullet points untuk readability
   - Include images dengan alt text

5. **Internal Linking**
   - Link ke artikel blog lain
   - Link ke service pages (jasa-website)
   - Link ke homepage

6. **Featured Image**
   - Ukuran: 1200x630px (optimal for social share)
   - Format: JPG atau PNG
   - File size: < 200KB (optimize!)
   - Alt text: descriptive & include keyword

---

## 🎯 Expected Google Search Results

Setelah deploy & indexing (1-7 hari), blog posts akan muncul seperti ini:

```
kardigi.tech › blog › tips-membuat-website
Tips Membuat Website untuk Bisnis | Blog KARDIGI
Jan 21, 2026 — Panduan lengkap cara membuat website untuk 
bisnis Anda. Mulai dari perencanaan, desain, hingga launching 
dengan budget terjangkau.
```

**Components:**
- **URL**: kardigi.tech › blog › [slug]
- **Title** (blue): Meta title atau H1 (60 chars)
- **Date**: Auto dari `created_at`
- **Description** (gray): Meta description (160 chars)

---

## 🔧 Maintenance Checklist

### Weekly:
- [ ] Check Google Search Console for errors
- [ ] Monitor crawl stats
- [ ] Check mobile usability issues

### Monthly:
- [ ] Update sitemap if needed (auto-generated)
- [ ] Review blog performance (impressions, clicks)
- [ ] Check broken links
- [ ] Optimize slow pages

### After Publishing New Blog:
- [ ] Request indexing di Google Search Console
- [ ] Share di social media (untuk backlinks)
- [ ] Test Open Graph preview
- [ ] Internal linking dari artikel lama

---

## 📞 Support

Jika ada issue dengan SEO atau Google Search Console:
1. Check browser console untuk errors
2. Validate schema.org di Google Rich Results Test
3. Test Open Graph di Facebook Debugger
4. Check sitemap di `/sitemap.xml`

**Contact**: kardigi.id@gmail.com
**WhatsApp**: +6289509951772

---

## 🎉 Summary

✅ **SEO-Ready**: Website fully optimized untuk search engines
✅ **Dynamic Sitemap**: Auto-generated dengan blog posts
✅ **Rich Snippets**: Schema.org structured data
✅ **Social Share**: Open Graph & Twitter Cards
✅ **Blog SEO Tools**: Focus keyword, preview, word count
✅ **Mobile-Friendly**: Responsive design
✅ **Fast Loading**: Optimized images & code

**Next Steps:**
1. Deploy website ke production
2. Verify di Google Search Console
3. Submit sitemap
4. Publish first blog post
5. Request indexing
6. Monitor hasil dalam 1-7 hari

🚀 **Ready for SEO Success!**
