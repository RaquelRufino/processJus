# # from http.server import BaseHTTPRequestHandler, HTTPServer
# # from urllib.parse import urljoin
import sys
sys.path.append("..")
from crawlers.esaj import search_process
import json
# # class GP(BaseHTTPRequestHandler):

# #     def _set_headers(self):
# #         self.send_response(200)
# #         self.send_header('Content-type', 'application/json')
# #         self.end_headers()

# #     def do_HEAD(self):
# #         self._set_headers()

# #     # def do_POST(self):
# #     #     self._set_headers().getheader('content-length', 0)
# #     #     form = cgi.FieldStorage(
# #     #         fp=self.rfile,
# #     #         headers=self.headers,
# #     #         environ={'REQUEST_METHOD': 'POST'}
# #     #     )
# #     #     print form.getvalue("number")
# #     #     print form.getvalue("state")
# #     def do_POST(self):
# #         #self._set_headers().getheader('content-length', 0)
# #         content_len = int(self.headers.getheader('content-length', 0))
# #         post_body = self.rfile.read(content_len)
# #         #ProcessSpider.parse(post_body)
# #         search_process(None)
# #         #print post_body
      
# # def run(server_class=HTTPServer, handler_class=GP, port=8088):
# #     server_address = ('', port)
# #     httpd = server_class(server_address, handler_class)
# #     print ('Server running at localhost:8088...')
# #     httpd.serve_forever()

# # run()

# # import SimpleHTTPServer
# # import SocketServer

# # PORT = 8088

# # class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

# #     def do_POST(self):
# #       content_len = int(self.headers.getheader('content-length', 0))
# #       post_body = self.rfile.read(content_len)
# #       print post_body

# # Handler = ServerHandler

# # httpd = SocketServer.TCPServer(("", PORT), Handler)

# # print "serving at port", PORT
# # httpd.serve_forever()
# from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
# from optparse import OptionParser
# import sys
# sys.path.append("..")
# from crawlers.esaj import search_process

# class RequestHandler(BaseHTTPRequestHandler):
       
#     def do_POST(self):
        
#         request_path = self.path

#         request_headers = self.headers
#         content_length = request_headers.getheaders('content-length')
#         length = int(content_length[0]) if content_length else 0
        
#         print(self.rfile.read(length))
#         print search_process(self.rfile.read(length))
        
#         self.send_response(200)
        
# def main():
#     port = 8082
#     print('Listening on localhost:%s' % port)
#     server = HTTPServer(('', port), RequestHandler)
#     server.serve_forever()

        
# if __name__ == "__main__":
#     parser = OptionParser()
#     parser.usage = ("Creates an http-server that will echo out any GET or POST parameters\n"
#                     "Run:\n\n"
#                     "   reflect")
#     (options, args) = parser.parse_args()
    
#     main()

from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        #print (search_process(body.decode()))
        response.write(body)
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()