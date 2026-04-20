import sqlite3
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS products(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		nama TEXT,
		harga INTEGER,
		stok INTEGER
	)
	""")
	cursor.execute("""
	CREATE TABLE IF NOT EXISTS users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		username TEXT,
		password TEXT
		
	)
	""")
	conn.commit()