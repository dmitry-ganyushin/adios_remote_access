import paramiko
paramiko.util.log_to_file(r'C:\Users\yvg\paramiko.log')
username = "hpcgany1"
key_password = "aUgmetpamcirj21()n"
file_path = r"c:\users\yvg\.ssh\id_rsa2048"
hostname = "login.hpc.cam.ac.uk"
port = 22
password = input("OTP password:")
key_password = "aUgmetpamcirj21()n"
file_path = r"c:\users\yvg\.ssh\id_rsa2048"
pkey = paramiko.RSAKey.from_private_key_file(file_path, password=key_password)

transport = paramiko.Transport((hostname, port))
transport.connect()

# auth the public key as usual, auth service now is activated on server
transport.auth_publickey(username=username, key=pkey)

# try to send another userauth request without request auth service
m = paramiko.Message()
m.add_byte(paramiko.common.cMSG_USERAUTH_REQUEST)
m.add_string(username)
m.add_string('ssh-connection')
m.add_string('password')
m.add_boolean(False)
py3_password = password
m.add_string(py3_password)
transport.packetizer.send_message(m)

# now it works! : )
sftp_client = paramiko.SFTPClient.from_transport(transport)

remote_file = sftp_client.file("/home/hpcgany1/setup_daos.sh", 'r')
# remote_file1 = sftp.file(filepath1, 'r')
remote_file.seek(0)  # Move the file pointer to the desired starting byte
data = remote_file.read(100)  # Read the specified chunk of data
print(data)