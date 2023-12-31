import paramiko
import time
import getpass

# paramiko.util.log_to_file("paramiko.log")
start_byte = 0  # Starting byte index (0 for the beginning of the file)
end_byte = 1024  # Ending byte index (e.g., 1023 for the first 1KB)
# Open a transport
# host, port = "localhost", 22
# transport = paramiko.Transport((host, port))
# # Auth username,password = "bar","foo"
# transport.connect(None, "", "")

REMOTE_HOST = input("hostname: ")
#REMOTE_HOST = "localhost"
transport = paramiko.Transport((REMOTE_HOST, 22))

user = input("Username: ")
key = input("Key:")
if key != "":
    key_passphrase = input("Key passphrase:")
try:
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)
#user = ""
#password = ""

if key == "":
    transport.connect(None, user, password)
else:
    private_key = paramiko.RSAKey.from_private_key_file(key, password=key_passphrase)
    transport.connect(None, user, password, pkey=private_key)

# Go!
sftp = paramiko.SFTPClient.from_transport(transport)  # data0
# sftp1 = paramiko.SFTPClient.from_transport(transport) # data1
# Download
#filepath = "/home/ganyush/adiostests/test.bp/md.idx"  # data.0
filepath = "/ccs/home/ganyushin/data" # data.0
localpath = "/home/ganyush/adiostests/temp.txt"
# sftp.get(filepath,localpath)
start = time.time()
remote_file = sftp.file(filepath, 'r')
# remote_file1 = sftp.file(filepath1, 'r')
remote_file.seek(start_byte)  # Move the file pointer to the desired starting byte
data = remote_file.read(end_byte - start_byte + 1)  # Read the specified chunk of data
print(data)
# remote_file1.seek(start_byte)  # Move the file pointer to the desired starting byte
# data = remote_file1.read(end_byte - start_byte + 1)  # Read the specified chunk of data
# print(data)
print(time.time() - start)
remote_file.seek(end_byte + 1)  # Move the file pointer to the desired starting byte
data = remote_file.read(end_byte - start_byte + 1)  # Read the specified chunk of data
print(data)
with open(localpath, 'wb') as local_file:
    local_file.write(data)  # Write the downloaded data to the local file
# Close if sftp:
sftp.close()
if transport:
    transport.close()
