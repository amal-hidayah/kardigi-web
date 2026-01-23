import sqlite3

# Koneksi ke database
conn = sqlite3.connect('amaljaya.db')
c = conn.cursor()

# Cek apakah kolom 'slug' sudah ada di tabel BlogPost
c.execute("PRAGMA table_info(BlogPost)")
columns = [col[1] for col in c.fetchall()]

if 'slug' not in columns:
    print('Kolom slug belum ada, menambahkan...')
    c.execute("ALTER TABLE BlogPost ADD COLUMN slug TEXT UNIQUE")
    conn.commit()
    print('Kolom slug berhasil ditambahkan!')
else:
    print('Kolom slug sudah ada.')

conn.close()
