import time
import pycurl

from io import BytesIO

buf = BytesIO()
options = {
    pycurl.URL: 'sftp://localhost:3022/home/ganyush/mach.txt',
    pycurl.WRITEFUNCTION: buf.write,
    pycurl.NOPROGRESS: 1,
    pycurl.USERPWD: 'ganyush:Ugmetpamcirj21*(',
    pycurl.RANGE: "0-200",
}

c = pycurl.Curl()
for (k, v) in options.items():
    c.setopt(k, v)
t0 = time.perf_counter()
c.perform()
print(':TIME:\n' + str(time.perf_counter() - t0))
c.setopt(pycurl.URL, 'sftp://localhost/home/ganyush/mach.txt')
c.setopt(pycurl.PORT, 3022)
c.setopt(pycurl.RANGE, "0-100")

t0 = time.perf_counter()
c.perform()
print(':TIME:\n' + str(time.perf_counter() - t0))
print(buf.getvalue())