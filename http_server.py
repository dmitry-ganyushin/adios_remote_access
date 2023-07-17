import sys
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
        # print("HEADERS:")
        # print(self.headers)
        # print("COMMAND:")
        # print(self.command)
        # print("PATH:")
        # print(self.path)
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        filepath = self.path
        remote_file = sftp.file(filepath, 'r')
        header = self.headers["Range"]
        if header:
            ranges = header.split("=")[1].split("-")
            start_byte = int(ranges[0])
            end_byte = int(ranges[1])
            #TODODG
            # make batches
            remote_file.seek(start_byte)  # Move the file pointer to the desired starting byte
            data = remote_file.read(end_byte - start_byte + 1)

            """send data back"""
            self.wfile.write(data)
            return

        header = self.headers["Content-Length"]

        if header:
            data = remote_file.stat()

            """send data back"""
            self.wfile.write(bytes(str(int(data.st_size)), "utf-8)"))
            return

        self.wfile.write("Ok".encode("utf-8"))

##################################################

REMOTE_HOST = input("hostname: ")

if sys.argv[1] == "--auth=2":
    auth_key = input("Auth key:")
    key_password = ""
    try:
        key_password = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    pkey = paramiko.RSAKey.from_private_key_file(auth_key, password=key_password)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

user = input("Username: ")
try:
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)

if __name__ == "__main__":
    if sys.argv[1] == "--auth=2":
        print("connecting ...")
        client.connect( hostname=REMOTE_HOST, username=user, pkey=pkey, password=password)
        print("connected")
        sftp = client.open_sftp()
    else:
        #REMOTE_HOST = "localhost"
        transport = paramiko.Transport((REMOTE_HOST, 22))
        #user = ""
        #password = ""
        transport.connect(None, user, password)
        # Go!
        sftp = paramiko.SFTPClient.from_transport(transport)

    server = HTTPServer((HOST, PORT), ADIOS_HTTP_Request)
    print("Server now serving ...")

    server.serve_forever()

    server.server_close()
    print("Server stopped")
