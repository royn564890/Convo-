from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Facebook par comment karne ka function
def post_comment(post_id, comment_text, access_token):
    url = f"https://graph.facebook.com/v15.0/{post_id}/comments"
    payload = {"message": comment_text}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return {"status": "success", "response": response.json()}
        else:
            return {"status": "failed", "error": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# API Route jo comments bhejega
@app.route('/comment', methods=['POST'])
def comment_api():
    data = request.json
    post_id = data.get("post_id")
    comment_text = data.get("comment_text")
    access_token = data.get("access_token")
    
    # Input validate karna
    if not post_id or not comment_text or not access_token:
        return jsonify({"error": "Missing parameters"}), 400
    
    result = post_comment(post_id, comment_text, access_token)
    return jsonify(result)

# Flask app chalana
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
