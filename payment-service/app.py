from flask import Flask, request, jsonify
app = Flask(__name__)

@app.post('/pay')
def pay():
    data = request.get_json(force=True)
    amount = data.get('amount', 0)
    method = data.get('method', 'card')
    return jsonify({"status": "ok", "amount": amount, "method": method})

app.run(host='0.0.0.0', port=3002)
