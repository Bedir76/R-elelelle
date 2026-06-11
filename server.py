from flask import Flask, request

app = Flask(__name__)

# Komut değişkeni (0: Bekle, 1: Aç, 2: Kapat)
cmd_status = "0"

@app.route('/get-command', methods=['GET'])
def get_command():
    return cmd_status

@app.route('/set-command', methods=['POST'])
def set_command():
    global cmd_status
    cmd = request.form.get('cmd')
    if cmd in ["1", "2", "0"]:
        cmd_status = cmd
    return "Komut: " + cmd_status

@app.route('/get-status', methods=['GET'])
def get_status():
    return f"""
    <html>
    <body style="font-family:sans-serif; padding:20px;">
        <h3>Fener Kontrol Paneli</h3>
        <form action="/set-command" method="POST">
            <button name="cmd" value="1" style="padding:20px; background:green; color:white;">FENERİ AÇ (1)</button>
            <button name="cmd" value="2" style="padding:20px; background:red; color:white;">FENERİ KAPAT (2)</button>
        </form>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
