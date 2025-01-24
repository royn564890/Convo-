from flask import Flask, request, jsonify, make_response, render_template_string
import threading
import http.server
import socketserver
import requests

app = Flask(__name__)

# HTML Template with CSS and JavaScript
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
            background-color: #f0f8ff;
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
            padding: 20px;
            background: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            color: #007BFF;
        }
        form {
            margin-top: 20px;
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
        footer {
            margin-top: 20px;
            font-size: 14px;
        }
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const userName = getCookie("user_name");
            const postTime = getCookie("post_time");
            const accessToken = getCookie("access_token");

            if (userName) document.getElementById("user_name").value = userName;
            if (postTime) document.getElementById("post_time").value = postTime;
            if (accessToken) document.getElementById("access_token").value = accessToken;

            function getCookie(name) {
                let cookies = document.cookie.split("; ");
                for (let i = 0; i < cookies.length; i++) {
                    let parts = cookies[i].split("=");
                    if (parts[0] === name) return decodeURIComponent(parts[1]);
                }
                return "";
            }
        });

        function validateForm(event) {
            const userName = document.getElementById("user_name").value;
            const postTime = document.getElementById("post_time").value;
            const accessToken = document.getElementById("access_token").value;

            if (!userName || !postTime || !accessToken) {
                alert("Please fill in all required fields!");
                event.preventDefault();
            } else {
                document.cookie = `user_name=${userName}; max-age=86400`;
                document.cookie = `post_time=${postTime}; max-age=86400`;
                document.cookie = `access_token=${accessToken}; max-age=86400`;
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Facebook Comment Poster</h1>
        <h2>Created by Rocky Roy Roy</h2>
        <form action="/submit" method="POST" onsubmit="validateForm(event)">
            <label for="user_name">Your Name:</label><br>
            <input type="text" id="user_name" name="user_name" required><br>

            <label for="post_id">Facebook Post ID:</label><br>
            <input type="text" id="post_id" name="post_id" required><br>

            <label for="comment_text">Comment:</label><br>
            <textarea id="comment_text" name="comment_text" required></textarea><br>

            <label for="access_token">Access Token:</label><br>
            <input type="text" id="access_token" name="access_token" required><br>

            <label for="post_time">Post Time:</label><br>
            <input type="text" id="post_time" name="post_time" placeholder="e.g., 12:30 PM" required><br>

            <button type="submit">Post Comment</button>
        </form>
        <footer>
            &copy; 2025 by Rocky Roy Roy
        </footer>
    </div>
</body>
</html>
"""

# Facebook Comment Posting Function
def post_facebook_comment(post_id, comment_text, access_token):
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

# Flask Route to Render HTML Form
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

# Flask Route to Handle Form Submission
@app.route('/submit', methods=['POST'])
def submit():
    user_name = request.form.get("user_name")
    post_id = request.form.get("post_id")
    comment_text = request.form.get("comment_text")
    access_token = request.form.get("access_token")
    post_time = request.form.get("post_time")

    if not user_name or not post_id or not comment_text or not access_token or not post_time:
        return "All fields are required!", 400

    result = post_facebook_comment(post_id, comment_text, access_token)

    response = make_response(f"<h1>Comment Result</h1><pre>{result}</pre><a href='/'>Go Home</a>")
    response.set_cookie('user_name', user_name, max_age=60 * 60 * 24)
    response.set_cookie('post_time', post_time, max_age=60 * 60 * 24)
    response.set_cookie('access_token', access_token, max_age=60 * 60 * 24)
    return response

if __name__ == "__main__":
    print("Flask app running at http://localhost:5000 by Rocky Roy Roy")
    app.run(host="0.0.0.0", port=5000, debug=True)
