import os
from sqlalchemy import create_url

# Render sẽ cung cấp biến này trong bảng điều khiển
DATABASE_URL = os.getenv("DATABASE_URL")

# Chỉnh sửa một chút nếu chuỗi bắt đầu bằng postgres:// (SQLAlchemy yêu cầu postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)