"""
Migration script to add SEO fields to BlogPost table
- meta_title (60 chars)
- focus_keyword (100 chars)
"""
from app import app, db, BlogPost
import sys

def migrate_blog_seo_fields():
    with app.app_context():
        # Check if columns already exist
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('blog_post')]
        
        print("Current columns:", columns)
        
        # Add new columns if they don't exist
        if 'meta_title' not in columns:
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE blog_post ADD COLUMN meta_title VARCHAR(60)'))
                    conn.commit()
                print("✅ Added meta_title column")
            except Exception as e:
                print(f"⚠️ meta_title column might already exist or error: {e}")
        else:
            print("ℹ️ meta_title column already exists")
        
        if 'focus_keyword' not in columns:
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE blog_post ADD COLUMN focus_keyword VARCHAR(100)'))
                    conn.commit()
                print("✅ Added focus_keyword column")
            except Exception as e:
                print(f"⚠️ focus_keyword column might already exist or error: {e}")
        else:
            print("ℹ️ focus_keyword column already exists")
        
        print("\n✨ Migration completed!")
        print("Database is ready for new SEO features:")
        print("  - Meta Title (custom SEO title)")
        print("  - Focus Keyword (Yoast-like SEO optimization)")

if __name__ == '__main__':
    try:
        migrate_blog_seo_fields()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\nIf you get errors, you can manually run these SQL commands:")
        print("  ALTER TABLE blog_post ADD COLUMN meta_title VARCHAR(60);")
        print("  ALTER TABLE blog_post ADD COLUMN focus_keyword VARCHAR(100);")
        sys.exit(1)
