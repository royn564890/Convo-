import http.server
import socketserver
import threading
import requests

# HTTP Server ka code
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # HTTP server response
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
            <h1>Facebook Comment Poster</h1>
            <form method="POST" action="/post_comment">
                <label for="post_id">Facebook Post ID:</label><br>
                <input type="text" id="post_id" name="post_id" required><br><br>
                
                <label for="comment">Comment:</label><br>
                <textarea id="comment" name="comment" required></textarea><br><br>
                
                <label for="access_token">Access Token:</label><br>
                <input type="text" id="access_token" name="access_token" required><br><br>
                
                <button type="submit">Post Comment</button>
            </form>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

    def do_POST(self):
        # Handle POST requests for posting comments
        if self.path == "/post_comment":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            form_data = dict(item.split('=') for item in post_data.split('&'))
            post_id = form_data.get("post_id")
            comment = form_data.get("comment")
            access_token = form_data.get("access_token")

            # Post the Facebook comment
            result = post_facebook_comment(post_id, comment, access_token)

            # Send response to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Facebook Comment Poster</title>
            </head>
            <body>
                <h1>Result</h1>
                <pre>{result}</pre>
                <a href="/">Go Back</a>
            </body>
            </html>
            """
            self.wfile.write(response_html.encode('utf-8'))

# Server chalana
def start_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Server chal raha hai: http://localhost:{PORT}")
        httpd.serve_forever()

# Facebook par comment karne ka function
def post_facebook_comment(post_id, comment, access_token):
    url = f"https://graph.facebook.com/v15.0/{post_id}/comments"
    payload = {"message": comment}
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return f"[+] Comment successfully posted: {comment}"
        else:
            return f"[x] Error while posting comment: {response.text}"
    except Exception as e:
        return f"[!] An error occurred: {e}"

# Main Function
if __name__ == "__main__":
    # HTTP Server ko alag thread mein chalana
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    print("Server is running at http://localhost:4000")
    print("Press Ctrl+C to stop the server.")
    server_thread.join()
