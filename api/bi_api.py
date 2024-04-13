import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

class EventAPIHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/events':
            try:
                with open('result.json', 'r') as f:
                    data = json.load(f)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'No events data available. Please run the scraper first.'}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'Endpoint not found.'}).encode())

if __name__ == "__main__":
    server_address = ('', 9006)
    httpd = HTTPServer(server_address, EventAPIHandler)
    print(f"API server running on port 9006...")
    httpd.serve_forever()