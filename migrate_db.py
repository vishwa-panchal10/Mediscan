import sqlite3

try:
    conn = sqlite3.connect('instance/mediscan.db')
    cursor = conn.cursor()
    
    # Check if user_id column exists
    cursor.execute("PRAGMA table_info(medicine)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'user_id' not in columns:
        print("Adding user_id column to medicine table...")
        cursor.execute("ALTER TABLE medicine ADD COLUMN user_id INTEGER REFERENCES user(id)")
        conn.commit()
        print("Migration successful.")
    else:
        print("user_id column already exists.")
        
    conn.close()
except Exception as e:
    print(f"Error: {e}")
