import sqlite3

try:
    conn = sqlite3.connect('instance/mediscan.db')
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(medicine)")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Medicine columns: {columns}")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables: {tables}")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
