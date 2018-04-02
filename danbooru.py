# -*- coding: UTF-8 -*-
import requests
import re
import time
import os
import logging
import threading

class DanbooruSpider:
    def __init__(self):
        self.url = 'https://danbooru.donmai.us'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/52.0.2743.116 Safari/537.36'
        }
        self.data = {}
        self.imgNum = 0
        self.lock = threading.Lock()
        self.logger = self.getLogger()


    def getLogger(self):
        logger = logging.getLogger('Danbooru')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('Danbooru/Logger.txt')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger = logging.getLogger('Danboorulogger')
        logger.setLevel(logging.DEBUG)

        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.info('start spider!')
        return logger

    def getRobots(self):
        with open('Danbooru/Roobots.txt', 'w') as f:
            robotRequest = requests.get(self.url + '/robots.txt')
            f.write(robotRequest.text)

    def getImgs(self, imgPage):
        pattern = re.compile('<img itemprop="thumbnailUrl" src="/data/preview/(.*?)" ', re.S)
        imgID = re.findall(pattern, imgPage.text)
        localPath = 'Danbooru/media/' + time.strftime('%Y-%m-%d-%H-%M', time.localtime())
        t = []
        i = 0
        if not os.path.exists(localPath):
            os.mkdir(localPath)
        for url in imgID:
            i+=1
            imgUrl = self.url + '/data/' + url
            type = re.findall(r'^.*\.(.*?)$', imgUrl)
            tn = threading.Thread(target=self.writeImg,args=(imgUrl,type[0],localPath,))
            t.append(tn)
        for th in t:
            th.start()
        for i in t:
            i.join()
        self.logger.info("本次spider执行完毕！")

    def writeImg(self, url, imgType, localPath):
        with self.lock:
            self.imgNum += 1
            print(self.imgNum)
        num = self.imgNum
        img = requests.get(url, headers=self.headers)
        self.logger.info("正在写入" + url + "\t编号：" + str(num))
        if img.text.startswith('<!DOCTYPE html>'):
            self.logger.warning("编号：" + str(num) + '\t无法获得图片！')
            return False
        with open(localPath + '/' + str(num) + '.' + imgType, 'wb') as f:
            f.write(img.content)
            self.logger.info("编号：" + str(num) + "\t写入完成！")
            return True

    def main(self):
        # self.getRobots()
        # self.getMainPage()
        r = requests.get('https://danbooru.donmai.us', headers=self.headers)
        self.getImgs(r)


if __name__ == '__main__':
    d = DanbooruSpider()
    d.main()
