import socket
import http.client

host = "localhost"
port = 9999
# construct your headers; maybe add a keepalive header here to avoid the remote server closing the connection
headers = {}
# create your connection object
conn = http.client.HTTPSConnection(host, port=port, timeout=600)
conn.connect()
# Now you will need to access the socket object of your connection; how you access this will vary depending on the library you use
s = conn.sock
# Set the following socket options (feel free to play with the values to find what works best for you)
# SO_KEEPALIVE: 1 => Enable TCP keepalive
# TCP_KEEPIDLE: 60 => Time in seconds until the first keepalive is sent
# TCP_KEEPINTVL: 60 => How often should the keepalive packet be sent
# TCP_KEEPCNT: 100 => The max number of keepalive packets to send
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 60)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 100)
conn.request("GET", "/endpoint", {}, headers)
response = conn.getresponse()
data = response.read()