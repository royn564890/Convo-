import http.server
import socketserver
import threading
import requests

# HTTP Server ka code
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Server chal raha hai - Facebook Comment Poster")

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
            print(f"[+] Comment successfully post hua: {comment}")
        else:
            print(f"[x] Comment post karne mein error: {response.text}")
    except Exception as e:
        print(f"[!] Error hua: {e}")

# Main Function
if __name__ == "__main__":
    # HTTP Server ko alag thread mein chalana
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Sample Facebook comment karna (real data replace karein)
    post_id = "POST_ID"  # Yahan apna Facebook post ID dalen
    comment = "Yeh ek test comment hai"  # Apna comment yahan likhein
    access_token = "ACCESS_TOKEN"  # Yahan apna access token dalen

    # Comment post karne ke liye function call karein
    post_facebook_comment(post_id, comment, access_token)
