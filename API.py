from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# --- Koneksi ke Database ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tb_cuaca"
)

@app.route('/', methods=['GET'])
def get_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_cuaca ORDER BY id DESC LIMIT 10")  # ambil 10 data terakhir
    data = cursor.fetchall()

    if not data:
        return jsonify({"message": "Belum ada data"}), 404

    # Ambil semua nilai suhu, humid, dan lux
    suhu_list = [row['suhu'] for row in data]
    humid_list = [row['humid'] for row in data]
    lux_list = [row['lux'] for row in data]

    result = {
        "jumlah_data": len(data),
        "suhumax": max(suhu_list),
        "suhumin": min(suhu_list),
        "suhurata": round(sum(suhu_list) / len(suhu_list), 2),
        "humidmax": max(humid_list),
        "humidmin": min(humid_list),
        "luxmax": max(lux_list),
        "luxmin": min(lux_list),
        "data_terbaru": data
    }

    return jsonify(result)

if __name__ == '__main__':
    print("🚀 API Flask berjalan di http://127.0.0.1:5000/")
    app.run(debug=True)