from flask import Flask, send_file, request, jsonify
import os
import threading
import time
import requests

app = Flask(__name__)

# Serve static files from the "public" directory
app.static_folder = os.path.join(os.path.dirname(__file__), "public")

@app.route('/')
def index():
    return send_file(os.path.join(app.static_folder, "index.html"))

# Function to send Facebook messages
def send_fb_message(convo_id, message, access_token):
    try:
        url = f"https://graph.facebook.com/v15.0/{convo_id}/messages"
        payload = {
            "message": {"text": message},
        }
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return {"status": "success", "response": response.json()}
        else:
            return {"status": "failed", "error": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# API route to send message
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    convo_id = data.get("convo_id")
    message = data.get("message")
    access_token = data.get("access_token")

    if not convo_id or not message or not access_token:
        return jsonify({"error": "Missing parameters"}), 400

    result = send_fb_message(convo_id, message, access_token)
    return jsonify(result)

# Function to keep pinging the server
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while True:
        time.sleep(sleep_time)
        try:
            response = requests.get('http://localhost:3000', timeout=10)
            print(f"Pinged server with response: {response.status_code}")
        except requests.RequestException as e:
            print(f"Ping failed: {e}")

# Main function to run Flask server and ping thread
if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=3000, debug=True))
    flask_thread.start()

    # Start the ping function in a separate thread
    ping_thread = threading.Thread(target=ping_server)
    ping_thread.start()
