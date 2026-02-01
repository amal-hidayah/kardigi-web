"""
SEO Checker Script - Test all URLs and generate report
Checks: Title, Description, OG tags, Canonical, Schema, Images
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

BASE_URL = "http://127.0.0.1:5000"

def check_page_seo(url):
    """Check SEO elements for a single page"""
    print(f"\n{'='*80}")
    print(f"🔍 Checking: {url}")
    print(f"{'='*80}")
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        issues = []
        warnings = []
        success = []
        
        # 1. Title Tag
        title = soup.find('title')
        if title:
            title_text = title.string
            title_len = len(title_text)
            if title_len < 30:
                warnings.append(f"⚠️ Title terlalu pendek ({title_len} chars): {title_text[:50]}")
            elif title_len > 60:
                warnings.append(f"⚠️ Title terlalu panjang ({title_len} chars): {title_text[:50]}...")
            else:
                success.append(f"✅ Title optimal ({title_len} chars): {title_text[:50]}")
        else:
            issues.append("❌ Title tag missing!")
        
        # 2. Meta Description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc_text = meta_desc.get('content', '')
            desc_len = len(desc_text)
            if desc_len < 120:
                warnings.append(f"⚠️ Meta description terlalu pendek ({desc_len} chars)")
            elif desc_len > 160:
                warnings.append(f"⚠️ Meta description terlalu panjang ({desc_len} chars)")
            else:
                success.append(f"✅ Meta description optimal ({desc_len} chars)")
        else:
            issues.append("❌ Meta description missing!")
        
        # 3. Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            success.append(f"✅ Canonical URL: {canonical.get('href', '')[:50]}")
        else:
            warnings.append("⚠️ Canonical URL missing")
        
        # 4. Open Graph Tags
        og_title = soup.find('meta', property='og:title')
        og_desc = soup.find('meta', property='og:description')
        og_image = soup.find('meta', property='og:image')
        
        if og_title and og_desc and og_image:
            success.append("✅ Open Graph tags complete")
        else:
            missing = []
            if not og_title: missing.append("og:title")
            if not og_desc: missing.append("og:description")
            if not og_image: missing.append("og:image")
            warnings.append(f"⚠️ Open Graph incomplete: missing {', '.join(missing)}")
        
        # 5. Twitter Card
        twitter_card = soup.find('meta', attrs={'name': 'twitter:card'})
        if twitter_card:
            success.append("✅ Twitter Card configured")
        else:
            warnings.append("⚠️ Twitter Card missing")
        
        # 6. Structured Data (Schema.org)
        schema_script = soup.find('script', type='application/ld+json')
        if schema_script:
            try:
                schema_data = json.loads(schema_script.string)
                schema_type = schema_data.get('@type', 'Unknown')
                success.append(f"✅ Schema.org: {schema_type}")
            except:
                warnings.append("⚠️ Schema.org JSON invalid")
        else:
            warnings.append("⚠️ Structured data missing")
        
        # 7. H1 Tag
        h1_tags = soup.find_all('h1')
        if len(h1_tags) == 0:
            issues.append("❌ No H1 tag found!")
        elif len(h1_tags) > 1:
            warnings.append(f"⚠️ Multiple H1 tags ({len(h1_tags)}) - should be only 1")
        else:
            success.append(f"✅ H1 tag: {h1_tags[0].get_text()[:50]}")
        
        # 8. Images without alt text
        images = soup.find_all('img')
        images_no_alt = [img for img in images if not img.get('alt')]
        if images_no_alt:
            warnings.append(f"⚠️ {len(images_no_alt)} images without alt text")
        else:
            success.append(f"✅ All {len(images)} images have alt text")
        
        # 9. Robots meta
        robots = soup.find('meta', attrs={'name': 'robots'})
        if robots:
            success.append(f"✅ Robots: {robots.get('content', '')}")
        else:
            warnings.append("⚠️ Robots meta missing")
        
        # Print Results
        for s in success:
            print(s)
        for w in warnings:
            print(w)
        for i in issues:
            print(i)
        
        # Score
        total_checks = len(success) + len(warnings) + len(issues)
        score = (len(success) / total_checks * 100) if total_checks > 0 else 0
        
        print(f"\n📊 SEO Score: {score:.1f}% ({len(success)} success, {len(warnings)} warnings, {len(issues)} issues)")
        
        return {
            'url': url,
            'score': score,
            'success': len(success),
            'warnings': len(warnings),
            'issues': len(issues)
        }
        
    except Exception as e:
        print(f"❌ Error checking {url}: {e}")
        return None

def check_sitemap():
    """Check dynamic sitemap"""
    print(f"\n{'='*80}")
    print(f"🗺️ Checking Sitemap")
    print(f"{'='*80}")
    
    try:
        response = requests.get(f"{BASE_URL}/sitemap.xml", timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        
        urls = soup.find_all('url')
        print(f"✅ Sitemap found with {len(urls)} URLs")
        
        for url in urls[:5]:  # Show first 5
            loc = url.find('loc').text if url.find('loc') else 'N/A'
            priority = url.find('priority').text if url.find('priority') else 'N/A'
            print(f"  • {loc} (priority: {priority})")
        
        if len(urls) > 5:
            print(f"  ... and {len(urls) - 5} more URLs")
            
        return len(urls)
        
    except Exception as e:
        print(f"❌ Error checking sitemap: {e}")
        return 0

def check_robots():
    """Check robots.txt"""
    print(f"\n{'='*80}")
    print(f"🤖 Checking robots.txt")
    print(f"{'='*80}")
    
    try:
        response = requests.get(f"{BASE_URL}/robots.txt", timeout=10)
        if response.status_code == 200:
            print("✅ robots.txt found")
            print(response.text)
        else:
            print(f"⚠️ robots.txt returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking robots.txt: {e}")

def main():
    print("\n" + "="*80)
    print("🎯 KARDIGI SEO CHECKER")
    print("="*80)
    print(f"Base URL: {BASE_URL}")
    print("\n⚠️ Make sure Flask server is running on http://127.0.0.1:5000")
    print("\nStarting SEO checks...\n")
    
    # Test pages
    pages = [
        '/',
        '/jasa-website',
        '/blog',
    ]
    
    results = []
    
    # Check each page
    for page in pages:
        url = urljoin(BASE_URL, page)
        result = check_page_seo(url)
        if result:
            results.append(result)
    
    # Check sitemap
    sitemap_count = check_sitemap()
    
    # Check robots.txt
    check_robots()
    
    # Final Summary
    print(f"\n{'='*80}")
    print("📈 SUMMARY")
    print(f"{'='*80}")
    
    if results:
        avg_score = sum(r['score'] for r in results) / len(results)
        total_success = sum(r['success'] for r in results)
        total_warnings = sum(r['warnings'] for r in results)
        total_issues = sum(r['issues'] for r in results)
        
        print(f"\n✅ Checked {len(results)} pages")
        print(f"📊 Average SEO Score: {avg_score:.1f}%")
        print(f"✅ Total Success: {total_success}")
        print(f"⚠️ Total Warnings: {total_warnings}")
        print(f"❌ Total Issues: {total_issues}")
        print(f"🗺️ Sitemap URLs: {sitemap_count}")
        
        print("\n💡 Recommendations:")
        if avg_score >= 80:
            print("   🎉 Excellent! Your SEO is in great shape.")
        elif avg_score >= 60:
            print("   👍 Good, but there's room for improvement. Check warnings above.")
        else:
            print("   ⚠️ Needs attention. Fix critical issues above.")
        
        if total_warnings > 0:
            print("   • Review and fix warnings for better optimization")
        if total_issues > 0:
            print("   • Fix critical issues immediately!")
        
        print("\n📚 Next Steps:")
        print("   1. Deploy to production (kardigi.tech)")
        print("   2. Verify ownership di Google Search Console")
        print("   3. Submit sitemap: https://kardigi.tech/sitemap.xml")
        print("   4. Request indexing untuk blog posts")
        print("   5. Monitor hasil dalam 1-7 hari")
        
        print(f"\n{'='*80}")
        print("✨ SEO Check Complete!")
        print(f"{'='*80}\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ SEO check cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
