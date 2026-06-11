from flask import Flask, request

app = Flask(__name__)

# Verileri tutan sözlük
anlik_veri = {
    "konum": "Konum bekleniyor...",
    "bildirim": "Henüz bildirim gelmedi..."
}

@app.route('/update', methods=['POST'])
def update():
    # Konum verisi: "20.33345, 30.93939" formatında gelir
    if 'lat' in request.form:
        anlik_veri["konum"] = request.form.get('lat')
    
    # Bildirim verisi: "Başlık: İçerik" formatında gelir
    if 'bildirim' in request.form:
        anlik_veri["bildirim"] = request.form.get('bildirim')
    
    return "OK", 200

@app.route('/get-status', methods=['GET'])
def get_status():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistem Paneli</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; line-height: 1.6; }}
            .box {{ border: 1px solid #ccc; padding: 15px; border-radius: 8px; margin-bottom: 10px; }}
            h3 {{ margin-top: 0; color: #333; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h3>📍 Konum</h3>
            <p style="color: blue; font-weight: bold;">{anlik_veri['konum']}</p>
        </div>
        <div class="box">
            <h3>🔔 Son Bildirim</h3>
            <p style="color: green;">{anlik_veri['bildirim']}</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

