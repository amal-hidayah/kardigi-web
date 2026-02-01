"""
Reset Database Script for Production
WARNING: This will DELETE all existing data!
Use this to create fresh database with correct schema
"""
import os
import sys

def reset_database_production():
    """Reset database di production dengan schema terbaru"""
    
    print("\n" + "="*80)
    print("⚠️  WARNING: DATABASE RESET")
    print("="*80)
    print("\nThis will DELETE all data:")
    print("  • All blog posts")
    print("  • All orders")
    print("  • All portfolio items")
    print("\nAre you sure? This cannot be undone!")
    print("="*80)
    
    confirm = input("\nType 'RESET' to confirm: ")
    
    if confirm != 'RESET':
        print("\n❌ Cancelled. Database not modified.")
        return
    
    print("\n🔄 Starting database reset...")
    
    try:
        from app import app, db
        
        with app.app_context():
            # Drop all tables
            print("📦 Dropping all existing tables...")
            db.drop_all()
            print("✅ All tables dropped")
            
            # Create all tables with new schema
            print("📦 Creating tables with new schema...")
            db.create_all()
            print("✅ All tables created")
            
            print("\n" + "="*80)
            print("✅ DATABASE RESET COMPLETE!")
            print("="*80)
            print("\nNew schema includes:")
            print("  ✅ BlogPost table with meta_title & focus_keyword")
            print("  ✅ Order table")
            print("  ✅ PortfolioWebsite table")
            print("\n📝 Next steps:")
            print("  1. Restart service: sudo systemctl restart kardigi")
            print("  2. Login to admin: /login")
            print("  3. Create new blog posts with SEO features")
            print("\n✨ Database is ready!")
            
    except Exception as e:
        print(f"\n❌ Error during reset: {e}")
        print("\nIf you see module import errors, make sure you're in the correct directory.")
        print("Run this from: ~/kardigi-web/")
        sys.exit(1)

if __name__ == '__main__':
    reset_database_production()
