from flask import Flask, request, jsonify, make_response, render_template_string
import threading
import http.server
import socketserver
import requests

# Flask App
app = Flask(__name__)

# HTML Template for Flask
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
    <form action="/submit" method="POST">
        <label for="user_name">Your Name:</label><br>
        <input type="text" id="user_name" name="user_name" required><br><br>

        <label for="post_id">Facebook Post ID:</label><br>
        <input type="text" id="post_id" name="post_id" required><br><br>

        <label for="comment_text">Comment:</label><br>
        <textarea id="comment_text" name="comment_text" required></textarea><br><br>

        <label for="access_token">Access Token:</label><br>
        <input type="text" id="access_token" name="access_token" required><br><br>

        <label for="post_time">Post Time:</label><br>
        <input type="text" id="post_time" name="post_time" placeholder="e.g., 12:30 PM" required><br><br>

        <button type="submit">Post Comment</button>
    </form>
    <hr>
    <h2>Welcome Back</h2>
    <p>If you've submitted before, your details are saved in cookies.</p>
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
    user_name = request.cookies.get('user_name')
    post_time = request.cookies.get('post_time')

    if user_name and post_time:
        return f"""
        <h1>Welcome back, {user_name}!</h1>
        <p>Last post time: {post_time}</p>
        <a href="/logout">Logout</a>
        """
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

    # Set cookies for user name and post time
    response = make_response(f"<h1>Comment Result</h1><pre>{result}</pre><a href='/'>Go Home</a>")
    response.set_cookie('user_name', user_name, max_age=60 * 60 * 24)  # Cookie valid for 1 day
    response.set_cookie('post_time', post_time, max_age=60 * 60 * 24)
    return response

# Flask Route to Logout (Clear Cookies)
@app.route('/logout')
def logout():
    response = make_response("<h1>You have been logged out!</h1><a href='/'>Go Home</a>")
    response.delete_cookie('user_name')
    response.delete_cookie('post_time')
    return response

# HTTP Server Handler
class MyHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Comment Poster</title>
        </head>
        <body>
            <h1>Welcome to HTTP Server</h1>
            <p>This is a simple HTTP server alongside the Flask app.</p>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        if self.path == "/post_comment":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(item.split('=') for item in post_data.split('&'))

            post_id = form_data.get("post_id")
            comment_text = form_data.get("comment_text")
            access_token = form_data.get("access_token")

            # Post the comment to Facebook
            result = post_facebook_comment(post_id, comment_text, access_token)

            # Respond with the result
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"<h1>Result</h1><pre>{result}</pre>".encode('utf-8'))

# Function to Run HTTP Server
def run_http_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHTTPHandler) as httpd:
        print(f"HTTP server running at http://localhost:{PORT}")
        httpd.serve_forever()

# Main Function to Run Both Servers
if __name__ == "__main__":
    # Start HTTP server in a separate thread
    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()

    print("Flask app running at http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
