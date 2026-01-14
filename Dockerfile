# 1. Ambil 'bahan dasar' OS yang sudah ada Python-nya
FROM python:3.9-slim

# 2. Tentukan folder kerja di dalam server nanti
WORKDIR /app

# 3. Copy file requirements.txt dulu untuk install library
COPY requirements.txt .

# 4. Jalankan perintah install library
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy semua file kode kamu (app.py, dll) ke dalam server
COPY . .

# 6. Beritahu server bahwa kita akan pakai port 5000
EXPOSE 5000

# 7. Perintah untuk menjalankan aplikasi kamu
# Kita pakai Gunicorn agar koneksi WebSocket stabil
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "app:app"]