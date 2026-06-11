from flask import Flask, request

app = Flask(__name__)

son_konum = "Veri bekleniyor..."

@app.route('/update', methods=['POST'])
def update():
    global son_konum
    lat = request.form.get('lat')
    lon = request.form.get('lon')
    son_konum = f"{lat},{lon}"
    return "OK"

@app.route('/get-konum', methods=['GET'])
def get_konum():
    return son_konum

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

