import psycopg2
import os
import json

DATABASE_URL = os.environ.get("DATABASE_URL")  # Render tự cung cấp khi gán biến môi trường

def init_state():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Tạo bảng state nếu chưa tồn tại
    cur.execute("""
    CREATE TABLE IF NOT EXISTS state (
        id SERIAL PRIMARY KEY,
        global_index INTEGER NOT NULL DEFAULT 0,
        folder_index JSONB NOT NULL DEFAULT '{}'::jsonb,
        processed_files JSONB NOT NULL DEFAULT '[]'::jsonb,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """)

    # Check record mặc định
    cur.execute("SELECT COUNT(*) FROM state")
    if cur.fetchone()[0] == 0:
        folder_index = {
            "nhieu item": 0,
            "kidshirt": 0,
            "1item": 0,
            "hieuungmautoi": 0,
            "khachtusua": 0
        }
        cur.execute(
            "INSERT INTO state (global_index, folder_index, processed_files) VALUES (%s, %s, %s)",
            (0, json.dumps(folder_index), json.dumps([]))
        )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Bảng state và record mặc định đã tạo xong")

if __name__ == "__main__":
    init_state()