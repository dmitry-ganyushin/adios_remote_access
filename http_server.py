from http.server import HTTPServer, BaseHTTPRequestHandler
import paramiko
import getpass

HOST = "127.0.0.1"
PORT = 9999

"""
Typical command
curl http://127.0.0.1:9999/home/ganyush/adiostests/test.bp/md.idx -i -H "Range: bytes=0-10"
"""

class ADIOS_HTTP_Request(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.headers)
        print(self.command)
        print(self.path)
        filepath = self.path
        remote_file = sftp.file(filepath, 'r')
        ranges = self.headers["Range"].split("=")[1].split("-")
        start_byte = int(ranges[0])
        end_byte = int(ranges[1])
        remote_file.seek(start_byte)  # Move the file pointer to the desired starting byte
        data = remote_file.read(end_byte - start_byte + 1)
        print(data)

        """send data back"""
        self.wfile.write(data)

transport = paramiko.Transport(("localhost", 22))
# Auth username,password = "bar","foo"

user = input("Username: ")
password = getpass.getpass(prompt='Password: ', stream=None)

transport.connect(None, user, password)
# Go!
sftp = paramiko.SFTPClient.from_transport(transport)

server = HTTPServer((HOST, PORT), ADIOS_HTTP_Request)
print("Server now serving ...")

server.serve_forever()

server.server_close()
print("Server stopped")


