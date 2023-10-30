import paramiko
k = paramiko.RSAKey.from_private_key_file(r"c:\users\yvg\.ssh\id_rsa2048", password="aUgmetpamcirj21()n")
transport = paramiko.Transport(("login.hpc.cam.ac.uk", 22))
transport.connect(None, username = "hpcgany1", pkey = k, password="693124")
c = paramiko.SFTPClient.from_transport(transport)
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("connecting")
#c.connect( hostname = "login.hpc.cam.ac.uk", username = "hpcgany1", pkey = k, password="014259")
print("connected")
# commands = [ "ls -l", "ls" ]
# for command in commands:
# 	print("Executing {}".format( command ))
# 	stdin , stdout, stderr = c.exec_command(command)
# 	print(stdout.read())
# 	print( "Errors")
# 	print(stderr.read())
# c.close()