
import socket
from urllib3.connection import HTTPConnection
import requests

# Note: if socket.TCP_KEEPIDLE is not defined, use 0x10.
HTTPConnection.default_socket_options += [
(socket.SOL_SOCKET, socket.SO_KEEPALIVE,1),
(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE ,60),
(socket.IPPROTO_TCP,socket.TCP_KEEPINTVL,60),
(socket.IPPROTO_TCP,socket.TCP_KEEPCNT,100),
]

for i in range (10):
    r=requests.get("http://localhost:9999").raw
    print(r)
