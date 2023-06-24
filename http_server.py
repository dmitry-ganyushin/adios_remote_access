from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 9999
class ADIOS_HTTP_Request(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.headers)
        print(self.command)
        print(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes("<html><body><h1>HELLO WORLD!</h1></body></html>", "utf-8"))

server = HTTPServer((HOST, PORT), ADIOS_HTTP_Request)
print("Server now serving ...")
print('Starting server, use <Ctrl-C> to stop')

server.serve_forever()
server.server_close()
print("Server stopped")


