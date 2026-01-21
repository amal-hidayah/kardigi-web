"""
Script untuk reset database - hapus semua data portfolio
Jalankan: python reset_database.py
"""
import os
import sys

# Pastikan import dari app.py
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, Referensi, Order

def reset_portfolio():
    """Hapus semua data referensi portfolio"""
    with app.app_context():
        # Hapus semua data referensi
        deleted_ref = Referensi.query.delete()
        db.session.commit()
        
        print(f"✅ Berhasil menghapus {deleted_ref} data referensi portfolio")
        print("📁 Database portfolio sekarang kosong")
        print("🎯 Admin bisa upload portfolio baru dari panel admin")

if __name__ == '__main__':
    confirm = input("⚠️  Yakin ingin reset database portfolio? (y/n): ")
    if confirm.lower() == 'y':
        reset_portfolio()
    else:
        print("❌ Reset dibatalkan")
