import http.server
import socketserver
import urllib.request
import urllib.error
import sqlite3
import json
import os

PORT = 8082

# Initialize Database
db_file = "chat_history.db"
conn = sqlite3.connect(db_file, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   sender TEXT,
                   text TEXT,
                   category TEXT,
                   confidenceScore REAL,
                   timestamp TEXT)''')
conn.commit()

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/messages':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            cursor.execute("SELECT sender, text, category, confidenceScore, timestamp FROM messages ORDER BY id ASC")
            rows = cursor.fetchall()
            messages = [{"sender": r[0], "text": r[1], "category": r[2], "confidenceScore": r[3], "timestamp": r[4]} for r in rows]
            self.wfile.write(json.dumps(messages).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/api/messages':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            cursor.execute("INSERT INTO messages (sender, text, category, confidenceScore, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (data.get('sender'), data.get('text'), data.get('category'), data.get('confidenceScore'), data.get('timestamp')))
            conn.commit()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "saved"}).encode('utf-8'))

        elif self.path == '/api/ProcessQuery':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            req = urllib.request.Request(
                "https://helpcenterfunction3-fdangsh0f0fcc0f4.centralindia-01.azurewebsites.net/api/ProcessQuery",
                data=post_data,
                headers={"Content-Type": "application/json"}
            )
            
            try:
                response = urllib.request.urlopen(req)
                resp_data = response.read()
                
                # Send the Azure response back to the frontend
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp_data)
                print("Proxied request to Azure successfully.")
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                self.end_headers()
                self.wfile.write(e.read())
                print(f"Azure HTTP Error: {e.code}")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode('utf-8'))
                print(f"Proxy Error: {e}")
        else:
            # If it's a POST to a file, just call standard handler (will fail typically)
            super().do_POST()

# Ensure older address bindings are freed
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    print(f"🚀 Server running on http://localhost:{PORT}")
    print("Azure Proxy is enabled for POST /api/ProcessQuery")
    print("SQLite Chat History is enabled for GET/POST /api/messages")
    httpd.serve_forever()
