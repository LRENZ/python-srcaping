import requests
from bs4 import BeautifulSoup
import os
from download import download
import urllib.request
import threading
from multiprocessing.dummy import Pool as  threadpool

class mzitu(download):






    def all_url(self, url):
        hreflist = []

        html = download.get(self,url,3)##调用request函数把套图地址传进去会返回给我们一个response
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find_all('a')
        for a in all_a:
            f= 0
            #title = a.get_text()
            #   print(u'开始保存：', title) ##加点提示不然太枯燥了
            try:
                path = str(f)  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
                self.mkdir(path)  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！

                os.chdir(os.path.join("D:\mzitu", path))
                print("began to download the pic:")
                href = a['href']
                hreflist.append(href)
                # self.html(href) ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
                # print("bagan to use the function html:")
                f= f+1
            except:
                print("something wrong")

        print("began to use the function html:")
        pool = threadpool()
        pool.map(self.html, hreflist)
        pool.close()
        pool.join()

    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        pageurl = []
        html = self.request(href)
        max_span = BeautifulSoup(html.text, 'lxml').find_all('span')[10].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            pageurl.append(page_url)
            #self.img(page_url) ##调用img函数
        pool = threadpool()
        pool.map(self.img, pageurl)
        pool.close()
        pool.join()



    def img(self, page_url): ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save1(img_url)

    def save(self, img_url): ##这个函数保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def save1(self,img_url):
        name = img_url[-9:-4]+".jpg"
        urllib.request.urlretrieve(img_url, name)


    def mkdir(self, path): ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join("D:\mzitu", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join("D:\mzitu", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url): ##这个函数获取网页的response 然后返回
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
        content = requests.get(url, headers=headers)
        return content
if __name__ == "__main__":
    Mzitu = mzitu()  ##实例化  #     ) ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
    Mzitu.all_url('http://www.mzitu.com/all')
