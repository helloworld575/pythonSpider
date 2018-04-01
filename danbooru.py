# -*- coding: UTF-8 -*-

import urllib.request

# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))
class DanbooruSpider:
    url = 'https://danbooru.donmai.us/'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)

    def getRobots(self):
        with open('Danbooru/DanbooruRoobots.txt', 'w') as f:
            robotRequest = urllib.request.Request(self.url + 'robots.txt', headers=self.headers)
            f.write(urllib.request.urlopen(robotRequest).read().decode('utf-8'))

    def getMainPage(self):
        self.response = urllib.request.urlopen(self.request)
        with open('Danbooru/DanbooruMainPage.txt','w') as f:
            f.write(self.response.read())

    def main(self):
        self.getRobots()
        self.getMainPage()

if __name__ == '__main__':
    d = DanbooruSpider()
    d.main()