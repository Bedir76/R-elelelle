From flask import Flask, request

app = Flask(__name__)

# Sunucu hafızasında verileri tutuyoruz
data_storage = {
    "konum": "Konum bekleniyor...",
    "bildirim": "Bildirim yok...",
    "komut": "0"  # 0: Bekle, 1: Ekran Aç/Kapat, 2: Feneri Aç
}

# 1. Android'den gelen konum ve bildirimleri kaydeder
@app.route('/update', methods=['POST'])
def update():
    if 'lat' in request.form:
        data_storage["konum"] = request.form.get('lat')
    if 'bildirim' in request.form:
        data_storage["bildirim"] = request.form.get('bildirim')
    return "OK", 200

# 2. Android'in sürekli kontrol ettiği komut adresi
@app.route('/get-command', methods=['GET'])
def get_command():
    cmd = data_storage["komut"]
    # Komutu gönderdikten sonra tekrar 0'a çekiyoruz (tek seferlik çalışması için)
    if cmd != "0":
        data_storage["komut"] = "0"
    return cmd

# 3. Senin komut vereceğin panel
@app.route('/set-command', methods=['POST'])
def set_command():
    cmd = request.form.get('cmd')
    if cmd in ["0", "1", "2"]:
        data_storage["komut"] = cmd
    return "Komut gönderildi: " + cmd

# 4. İzleme Paneli
@app.route('/get-status', methods=['GET'])
def get_status():
    return f"""
    <html>
    <head><meta charset="UTF-8"><title>Zewnd Kontrol</title></head>
    <body style="font-family:sans-serif; padding:20px;">
        <h3>📍 Konum: {data_storage['konum']}</h3>
        <h3>🔔 Bildirim: {data_storage['bildirim']}</h3>
        <hr>
        <h3>⚙️ Kontrol Paneli</h3>
        <form action="/set-command" method="POST">
            <button name="cmd" value="1" style="padding:10px;">Ekranı Uyandır</button>
            <button name="cmd" value="2" style="padding:10px;">Feneri Aç</button>
            <button name="cmd" value="0" style="padding:10px;">Sıfırla</button>
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
