from flask import Flask, request, jsonify
import threading
import time
import requests
import os

app = Flask(__name__)

# Function to post a comment on a Facebook post
def comment_on_post(post_id, comment_text, access_token):
    try:
        url = f"https://graph.facebook.com/v15.0/{post_id}/comments"
        payload = {"message": comment_text}
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            return {"status": "success", "response": response.json()}
        else:
            return {"status": "failed", "error": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# API route to send a comment
@app.route('/comment', methods=['POST'])
def post_comment():
    data = request.json
    post_id = data.get("post_id")
    comment_text = data.get("comment_text")
    access_token = data.get("access_token")

    if not post_id or not comment_text or not access_token:
        return jsonify({"error": "Missing parameters"}), 400

    result = comment_on_post(post_id, comment_text, access_token)
    return jsonify(result)

# Function to keep the server active by pinging itself
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
