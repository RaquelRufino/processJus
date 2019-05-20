from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import parse_qs
import cgi
import sys
# sys.path.append("/home/paz/Documentos/agoravai/processJus/processJus/spiders/process")
# from lib.process import ProcessSpider
#from processJus.spiders.process import ProcessSpider
class GP(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    # def do_POST(self):
    #     self._set_headers().getheader('content-length', 0)
    #     form = cgi.FieldStorage(
    #         fp=self.rfile,
    #         headers=self.headers,
    #         environ={'REQUEST_METHOD': 'POST'}
    #     )
    #     print form.getvalue("number")
    #     print form.getvalue("state")
    def do_POST(self):
        #self._set_headers().getheader('content-length', 0)
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        #ProcessSpider.parse(post_body)
        print post_body
      
def run(server_class=HTTPServer, handler_class=GP, port=8088):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Server running at localhost:8088...'
    httpd.serve_forever()

run()

# import SimpleHTTPServer
# import SocketServer

# PORT = 8088

# class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

#     def do_POST(self):
#       content_len = int(self.headers.getheader('content-length', 0))
#       post_body = self.rfile.read(content_len)
#       print post_body

# Handler = ServerHandler

# httpd = SocketServer.TCPServer(("", PORT), Handler)

# print "serving at port", PORT
# httpd.serve_forever()