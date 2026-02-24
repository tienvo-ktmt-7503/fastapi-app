import os
from flask import Flask, jsonify, render_template, request, session, redirect, Response, stream_with_context
from flask_cors import CORS
import psycopg2
import psycopg2.extras 
from psycopg2 import sql
import time
import json
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key") 
CORS(app) 

# --- CẤU HÌNH DATABASE (SỬA ĐỂ CHẠY CLOUD) ---
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    try:
        # Nếu có biến môi trường (Cloud), dùng URI. Nếu không (Local), dùng config
        if DATABASE_URL:
            # Fix lỗi format postgres:// của Render
            url = DATABASE_URL.replace("postgres://", "postgresql://", 1) if DATABASE_URL.startswith("postgres://") else DATABASE_URL
            return psycopg2.connect(url)
        else:
            import config
            return psycopg2.connect(**config.DB_CONFIG)
    except Exception as e:
        print("Lỗi kết nối Database:", e)
        return None

def try_db_login(user, pwd):
    try:
        if DATABASE_URL:
            # Tách lấy phần host/dbname từ URI gốc để login bằng user/pass mới
            base_url = DATABASE_URL.split('@')[1] 
            conn = psycopg2.connect(f"postgresql://{user}:{pwd}@{base_url}")
        else:
            import config
            conn = psycopg2.connect(dbname=config.DB_CONFIG["dbname"], user=user, password=pwd, host=config.DB_CONFIG["host"])
        conn.close()
        return True
    except:
        return False

# ... (Giữ nguyên các API: /api/login, /api/chart/feeding-daily, /api/metrics_fused, v.v.) ...
# XÓA BỎ: Luồng camera_worker, video_feed, và các dòng liên quan tới cv2.

if __name__ == '__main__':
    # Chạy Flask Server đơn thuần
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)