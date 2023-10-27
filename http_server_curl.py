import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import paramiko
import getpass
import pycurl
from io import BytesIO

HOST = "127.0.0.1"
PORT = 9999
"""
Typical command
curl http://127.0.0.1:9999/home/ganyush/adiostests/test.bp/md.idx -i -H "Range: bytes=0-10"
"""
buf = BytesIO
curl = pycurl.Curl()
class FastTransport(paramiko.Transport):

    def __init__(self, sock):
        super(FastTransport, self).__init__(sock)
        self.window_size = 2147483647
        self.packetizer.REKEY_BYTES = pow(2, 40)
        self.packetizer.REKEY_PACKETS = pow(2, 40)

class ADIOS_HTTP_PARAMIKO_Request(BaseHTTPRequestHandler):
    def do_GET(self):
        # print("HEADERS:")
        # print(self.headers)
        # print("COMMAND:")
        # print(self.command)
        # print("PATH:")
        # print(self.path)
        # self.protocol_version = 'HTTP/1.1'
        # self.send_response(200, 'OK')
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        filepath = self.path
        remote_file = sftp.file(filepath, 'r')
        remote_file.prefetch()
        header = self.headers["Range"]
        if header:
            ranges = header.split("=")[1].split("-")
            start_byte = int(ranges[0])
            end_byte = int(ranges[1])

            block_size = end_byte - start_byte + 1
            remote_file.seek(start_byte)
            """this is in fact ADIOS2 block. Expecting a reasonable size"""
            data = remote_file.read(block_size)
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

class ADIOS_HTTP_CURL_Request(BaseHTTPRequestHandler):
    def do_GET(self):
        filepath = self.path
        curl.setopt(pycurl.URL, "sftp://localhost:" + filepath)
        header = self.headers["Range"]
        if header:
            ranges = header.split("=")[1].split("-")
            """this is in fact ADIOS2 block. Expecting a reasonable size"""
            curl.setopt(pycurl.RANGE, ranges)
            data = curl.perform()
            """send data back"""
            self.wfile.write(data)
            return

        self.wfile.write("Ok".encode("utf-8"))


##################################################

def auth():
    REMOTE_HOST = input("hostname: ")
    pkey = None
    client = None

    if len(sys.argv) > 2 and sys.argv[2] == "--auth=2":
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
    return (client, REMOTE_HOST, user, pkey, password)

def main_paramiko(client, REMOTE_HOST, user, pkey, password):
    global sftp
    if len(sys.argv) > 2 and sys.argv[2] == "--auth=2":
        print("connecting ...")
        client.connect(hostname=REMOTE_HOST, username=user, pkey=pkey, password=password)
        print("connected")
        sftp = client.open_sftp()
    else:
        transport = FastTransport((REMOTE_HOST, 22))
        transport.connect(None, user, password)
        sftp = paramiko.SFTPClient.from_transport(transport)
    server = HTTPServer((HOST, PORT), ADIOS_HTTP_PARAMIKO_Request)
    try:
        # Listen for requests
        print("Server now serving ...")
        server.serve_forever()

    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()
        print("Server stopped")

def main_curl(REMOTE_HOST, user, pkey, password):
    global curl
    curl.setopt(pycurl.WRITEFUNCTION,  buf.write)
    curl.setopt(pycurl.NOPROGRESS, 1)
    curl.setopt(pycurl.USERPWD, password)
    server = HTTPServer((HOST, PORT), ADIOS_HTTP_CURL_Request)
    try:
        # Listen for requests
        print("Server now serving ...")
        server.serve_forever()

    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()
        print("Server stopped")



if __name__ == "__main__":
    (client, REMOTE_HOST, user, pkey, password) = auth()
    if len(sys.argv) > 1 and sys.argv[1] == "--mode=paramiko":
        main_paramiko(client, REMOTE_HOST, user, pkey, password)
    elif len(sys.argv) > 1 and sys.argv[1] == "--mode=curl":
        main_curl(REMOTE_HOST, user, pkey, password)