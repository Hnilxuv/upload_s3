# Sử dụng Python chính thức
FROM python:3.10-slim

# Đặt môi trường làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các dependency từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của ứng dụng vào container
COPY . .

# Chạy ứng dụng FastAPI khi container khởi động
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]