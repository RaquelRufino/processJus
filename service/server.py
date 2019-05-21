"""
API to run the crawler
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import sys
import json
sys.path.append("..")
import crawlers.esaj as esaj

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Making requisitions
    """

    def do_POST(self):
        """
        POST in API
        Example: 
        {    
            "number": "1002298-86.2015.8.26.0271",
            "state" : "sp"
        }
        """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        body = json.dumps(esaj.search_process(body.decode()))
        response.write(str(body).encode())
        self.wfile.write(response.getvalue())

Httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
Httpd.serve_forever()
