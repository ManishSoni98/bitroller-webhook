from flask import Flask, request, jsonify
import os

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "my_super_secret_9876")
MAIN_LTC_ADDRESS = os.getenv("MAIN_LTC_ADDRESS", "YOUR_MAIN_LTC_ADDRESS")

@app.route('/')
def home():
    return "✅ BitRoller Webhook Active!"

@app.route('/webhook/blockcypher', methods=['POST'])
def blockcypher_webhook():
    # Verify secret header
    if request.headers.get("X-Webhook-Secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    txid = data.get("hash")
    outputs = data.get("outputs", [])
    for output in outputs:
        if MAIN_LTC_ADDRESS in output.get("addresses", []):
            value = output.get("value", 0)
            ltc_value = value / 100000000  # satoshis → LTC
            print(f"✅ Deposit detected: TXID={txid} | Amount={ltc_value} LTC")
            return jsonify({"status": "deposit recorded"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)