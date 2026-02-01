#!/bin/bash

# Production Database Reset Script
# Run this on the server to reset database

echo "======================================================================"
echo "🔄 KARDIGI Database Reset for Production"
echo "======================================================================"
echo ""
echo "⚠️  WARNING: This will delete all existing data!"
echo ""
echo "What will be deleted:"
echo "  • All blog posts"
echo "  • All orders" 
echo "  • All portfolio items"
echo ""
echo "A fresh database will be created with the correct schema."
echo ""
read -p "Are you sure? Type 'yes' to continue: " confirm

if [ "$confirm" != "yes" ]; then
    echo ""
    echo "❌ Cancelled. No changes made."
    exit 0
fi

echo ""
echo "======================================================================"
echo "🔄 Starting database reset..."
echo "======================================================================"

# Navigate to project directory
cd ~/kardigi-web || exit 1

# Backup old database (just in case)
if [ -f "amaljaya.db" ]; then
    echo "📦 Creating backup of old database..."
    cp amaljaya.db "amaljaya.db.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup created"
fi

# Remove old database
echo "🗑️  Removing old database..."
rm -f amaljaya.db
echo "✅ Old database removed"

# Create new database with correct schema
echo "📦 Creating new database..."
python3 << EOF
from app import app, db

with app.app_context():
    db.create_all()
    print("✅ New database created with correct schema")
EOF

# Restart service
echo ""
echo "🔄 Restarting service..."
sudo systemctl restart kardigi

# Check status
echo ""
echo "======================================================================"
echo "✅ DATABASE RESET COMPLETE!"
echo "======================================================================"
echo ""
echo "New database schema includes:"
echo "  ✅ BlogPost (with meta_title & focus_keyword)"
echo "  ✅ Order"
echo "  ✅ PortfolioWebsite"
echo ""
echo "📝 Next steps:"
echo "  1. Visit: https://kardigi.tech"
echo "  2. Login: https://kardigi.tech/login"
echo "  3. Create portfolio items"
echo "  4. Create blog posts with SEO features"
echo ""
echo "✨ Ready to go!"
echo ""

# Check service status
sudo systemctl status kardigi --no-pager -l
