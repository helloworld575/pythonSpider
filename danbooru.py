# -*- coding: UTF-8 -*-
import requests
import re


class DanbooruSpider:
    url = 'https://danbooru.donmai.us'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/52.0.2743.116 Safari/537.36'
    }
    data = {}
    imgNum = 0

    def getRobots(self):
        with open('Danbooru/DanbooruRoobots.txt', 'w') as f:
            robotRequest = requests.get(self.url + '/robots.txt')
            f.write(robotRequest.text)

    def getMainPage(self):
        self.response = requests.get(self.url, params=self.data, headers=self.headers)
        print(self.response.text)

    def getImgs(self, imgPage):
        pattern = re.compile('<img itemprop="thumbnailUrl" src="/data/preview/(.*?)" ', re.S)
        imgID = re.findall(pattern, imgPage.text)
        for url in imgID:
            imgUrl = self.url+'/data/'+url
            type = re.findall(r'^.*\.(.*?)$', imgUrl)
            print("正在写入"+imgUrl+"编号："+str(self.imgNum))
            self.writeImg(imgUrl,type[0])
            print("编号："+str(self.imgNum-1)+"写入完成！")

    def writeImg(self, url, imgType):
        img = requests.get(url, headers=self.headers)
        with open('Danbooru/media/' + str(self.imgNum) + '.' + imgType, 'wb') as f:
            f.write(img.content)
            self.imgNum += 1

    def main(self):
        # self.getRobots()
        # self.getMainPage()
        r = requests.get('https://danbooru.donmai.us', headers=self.headers)
        self.getImgs(r)


if __name__ == '__main__':
    d = DanbooruSpider()
    d.main()
