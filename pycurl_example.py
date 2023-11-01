import time
import pycurl

from io import BytesIO

buf = BytesIO()
USER = ""
PASSWORD = ""
REMOTE_HOST = ""
PATH = ""
options = {
    pycurl.WRITEFUNCTION: buf.write,
    pycurl.NOPROGRESS: 1,
    pycurl.USERPWD: USER + ":" + PASSWORD,
    pycurl.VERBOSE: 1
#    pycurl.RANGE: "0-257",
}

c = pycurl.Curl()
for (k, v) in options.items():
    c.setopt(k, v)

c.setopt(c.URL, 'sftp://' + REMOTE_HOST + PATH)
c.setopt(c.NOBODY, 1)
c.setopt(pycurl.VERBOSE, 1)
c.perform()

c.setopt(c.NOBODY, 0)
print("size = {}".format(c.getinfo(c.CONTENT_LENGTH_DOWNLOAD)))
# download
c.reset()
c.setopt(c.URL, 'sftp://' + REMOTE_HOST + PATH)
c.setopt(pycurl.RANGE, "0-257")

#buf.seek(0)
#buf.truncate(0)

t0 = time.perf_counter()
c.setopt(pycurl.VERBOSE, 1)
c.setopt(pycurl.USERPWD, USER + ':' + PASSWORD)
c.setopt(pycurl.WRITEFUNCTION, buf.write)
c.perform()
print(':TIME:\n' + str(time.perf_counter() - t0))
print(buf.getvalue())


c.reset()
c.setopt(pycurl.USERPWD, USER + ':' + PASSWORD)
c.setopt(c.URL, 'sftp://' + REMOTE_HOST + PATH)
c.setopt(c.NOBODY, 1)
c.setopt(pycurl.VERBOSE, 1)
c.perform()

c.setopt(c.NOBODY, 0)
print("size = {}".format(c.getinfo(c.CONTENT_LENGTH_DOWNLOAD)))
