from urllib3 import HTTPConnectionPool

# pool = HTTPConnectionPool('ajax.googleapis.com', maxsize=1)
# r = pool.request('GET', '/ajax/services/search/web',
#                  fields={'q': 'python', 'v': '1.0'})
pool = HTTPConnectionPool('localhost', port=9999, maxsize=1)
# r = pool.request('GET', '/ajax/services/search/web',
#                  fields={'q': 'python', 'v': '1.0'})

for i in range(10):
    r = pool.request('GET', '/')

    print('Response Status:', r.status)

    # Header of the response
    print('Header: ',r.headers['content-type'])

    # Content of the response
    print('Python: ',len(r.data))

# r = pool.request('GET', '/ajax/services/search/web',
#              fields={'q': 'php', 'v': '1.0'})

r = pool.request('GET', '/')


# Content of the response
print('php: ',len(r.data))

print('Number of Connections: ',pool.num_connections)

print('Number of requests: ',pool.num_requests)
