from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Comment Poster</title>
</head>
<body>
    <h1>Facebook Comment Poster</h1>
    <form id="commentForm" method="POST" action="/comment">
        <label for="post_id">Facebook Post ID:</label><br>
        <input type="text" id="post_id" name="post_id" required><br><br>

        <label for="comment_text">Comment:</label><br>
        <textarea id="comment_text" name="comment_text" required></textarea><br><br>

        <label for="access_token">Access Token:</label><br>
        <input type="text" id="access_token" name="access_token" required><br><br>

        <button type="submit">Post Comment</button>
    </form>
    <hr>
    <h2>Instructions</h2>
    <p>1. Enter the Facebook Post ID where you want to comment.</p>
    <p>2. Enter the comment text.</p>
    <p>3. Provide a valid Facebook Graph API access token.</p>
    <p>4. Click "Post Comment" to submit the comment.</p>
</body>
</html>
"""

# Facebook comment posting function
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

# Route to render the HTML form
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# API route to handle comment submission
@app.route('/comment', methods=['POST'])
def comment_api():
    data = request.form
    post_id = data.get("post_id")
    comment_text = data.get("comment_text")
    access_token = data.get("access_token")
    
    # Validate input
    if not post_id or not comment_text or not access_token:
        return jsonify({"error": "Missing parameters"}), 400
    
    result = post_comment(post_id, comment_text, access_token)
    return jsonify(result)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
