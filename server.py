from flask import Flask, request

app = Flask(__name__)

# Anlık verileri tutan sözlük
anlik_veri = {
    "konum": "Konum bekleniyor...",
    "bildirim": "Henüz bildirim gelmedi..."
}

@app.route('/update', methods=['POST'])
def update():
    if 'lat' in request.form:
        anlik_veri["konum"] = f"{request.form.get('lat')}, {request.form.get('lon')}"
    if 'bildirim' in request.form:
        anlik_veri["bildirim"] = request.form.get('bildirim')
    return "OK"

@app.route('/get-status', methods=['GET'])
def get_status():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cihaz Paneli</title>
        <style>body {{ font-family: sans-serif; padding: 20px; }}</style>
    </head>
    <body>
        <h3>📍 Anlık Konum</h3>
        <p style="color: blue; font-size: 18px;">{anlik_veri['konum']}</p>
        <hr>
        <h3>🔔 Son Bildirim</h3>
        <p style="color: green; font-size: 18px;">{anlik_veri['bildirim']}</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

