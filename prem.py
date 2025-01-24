from flask import Flask, request, jsonify, make_response, render_template_string
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
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #007BFF;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            background-color: #007BFF;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Comment Poster</h1>
        <form action="/submit" method="POST">
            <label for="post_id">Facebook Post ID:</label><br>
            <input type="text" id="post_id" name="post_id" placeholder="Enter Facebook Post ID" required><br>

            <label for="comment_text">Comment:</label><br>
            <textarea id="comment_text" name="comment_text" placeholder="Enter your comment" required></textarea><br>

            <label for="access_token">Access Token:</label><br>
            <input type="text" id="access_token" name="access_token" placeholder="Enter your Access Token" required><br>

            <button type="submit">Post Comment</button>
        </form>
    </div>
</body>
</html>
"""

# Facebook Comment Posting Function
def post_comment_to_facebook(post_id, comment_text, access_token):
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

# Route for the Web Form
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Route to Handle Comment Submission
@app.route('/submit', methods=['POST'])
def submit():
    post_id = request.form.get("post_id")
    comment_text = request.form.get("comment_text")
    access_token = request.form.get("access_token")

    if not post_id or not comment_text or not access_token:
        return "All fields are required!", 400

    result = post_comment_to_facebook(post_id, comment_text, access_token)

    return render_template_string(f"""
    <h1>Comment Result</h1>
    <pre>{result}</pre>
    <a href="/">Go Back</a>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
