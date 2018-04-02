# import urllib3
#
# http = urllib3.PoolManager()
# request = http.request('GET','http://otome.me')
# print(request.status)
# print(request.data)
#
# import http.cookiejar, urllib.request
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = {'User-agent':user_agent}
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('https://danbooru.donmai.us')
# for item in cookie:
#     print(item.name+"="+item.value)

import requests
r = requests.get('https://danbooru.donmai.us/')
print(r.status_code)
print(r.text)
