import sqlite3

try:
    conn = sqlite3.connect('instance/mediscan.db')
    cursor = conn.cursor()
    
    print("Tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(f"- {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            
    conn.close()
except Exception as e:
    print(f"Error: {e}")
