import urllib3

http = urllib3.PoolManager()
request = http.request('GET','http://otome.me')
print(request.status)