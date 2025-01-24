from flask import Flask, request, jsonify, make_response, render_template_string
import threading
import http.server
import socketserver
import requests

app = Flask(__name__)

# HTML Template with JavaScript and Embedded Name "Rocky Roy Roy"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Comment Poster - By Rocky Roy Roy</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #6200ea;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        form {
            margin: 2rem auto;
            width: 50%;
            padding: 2rem;
            background: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border-radius: 8px;
        }
        form label {
            display: block;
            margin: 0.5rem 0 0.2rem;
        }
        form input, form textarea, form button {
            width: 100%;
            padding: 0.8rem;
            margin-bottom: 1rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }
        form button {
            background-color: #6200ea;
            color: white;
            border: none;
            cursor: pointer;
        }
        form button:hover {
            background-color: #4500c0;
        }
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            // Preload cookies if available
            const userName = getCookie("user_name");
            const postTime = getCookie("post_time");
            const accessToken = getCookie("access_token");

            if (userName) document.getElementById("user_name").value = userName;
            if (postTime) document.getElementById("post_time").value = postTime;
            if (accessToken) document.getElementById("access_token").value = accessToken;

            // Function to get a cookie by name
            function getCookie(name) {
                let cookies = document.cookie.split("; ");
                for (let i = 0; i < cookies.length; i++) {
                    let parts = cookies[i].split("=");
                    if (parts[0] === name) return decodeURIComponent(parts[1]);
                }
                return "";
            }
        });

        // Form validation before submission
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
    <header>
        <h1>Welcome to Facebook Comment Poster - By Rocky Roy Roy</h1>
    </header>
    <form action="/submit" method="POST" onsubmit="validateForm(event)">
        <label for="user_name">Your Name:</label>
        <input type="text" id="user_name" name="user_name" placeholder="Enter your name" required>

        <label for="post_id">Facebook Post ID:</label>
        <input type="text" id="post_id" name="post_id" placeholder="Enter the Facebook Post ID" required>

        <label for="comment_text">Comment:</label>
        <textarea id="comment_text" name="comment_text" placeholder="Write your comment here" required></textarea>

        <label for="access_token">Access Token:</label>
        <input type="text" id="access_token" name="access_token" placeholder="Enter your access token" required>

        <label for="post_time">Post Time:</label>
        <input type="text" id="post_time" name="post_time" placeholder="e.g., 12:30 PM" required>

        <button type="submit">Post Comment</button>
    </form>
</body>
</html>
"""

# Function to Post Facebook Comment
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

    # Post comment using the function
    result = post_facebook_comment(post_id, comment_text, access_token)

    # Set cookies for user name, post time, and access token
    response = make_response(f"<h1>Comment Result</h1><pre>{result}</pre><a href='/'>Go Home</a>")
    response.set_cookie('user_name', user_name, max_age=60 * 60 * 24)  # Cookie valid for 1 day
    response.set_cookie('post_time', post_time, max_age=60 * 60 * 24)
    response.set_cookie('access_token', access_token, max_age=60 * 60 * 24)
    return response

# Function to Run the Flask App
if __name__ == "__main__":
    print("Flask app running at http://localhost:5000 by Rocky Roy Roy")
    app.run(host="0.0.0.0", port=5000, debug=True)
