import urllib.request
import requests
import ssl
import re
import os

Pic_num = 1
class_Lis_num = 0


def test():
    return "Fu*k world! "

def make_file(toPath_Pic):
    file_name_list = ["class_1","class_2","class_3","class_4","class_7","class_8","class_9"]
    #创建文件名
    for name in file_name_list:
        Pic_Path = os.path.join(toPath_Pic,name)
        #print(Pic_Path)
        os.mkdir(Pic_Path)


def get_Html(url):
    # 请求体
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    Html = response.read()#.decode("utf-8")
    return Html


def get_Class_Lis(url):
    class_num = [1,2,3,4,7,8,9]
    # 直接构造class_url
    class_Lis = []
    class_Lis_True = []
    for num in class_num:
        class_Str = url + "/htm/piclist" + str(num) + "/"
        class_Str_True = url + "/htm/pic" + str(num) + "/"
        class_Lis.append(class_Str)
        class_Lis_True.append(class_Str_True)
    return class_Lis,class_Lis_True


def get_Page_Lis(class_url):
    #获取1个class的html
    html = get_Html(class_url)
    html = html.decode("utf-8")
    # 提取尾页num正则
    num = re.search(r"piclist[0-9]/(\d{3})\.htm\" class",html)
    urlNum = num.group(1)
    urlNum = int(urlNum)
    urlNum = urlNum + 1
    #利用取尾页字符串构造Page_Lis
    Page_Lis = []
    for num in range(urlNum):
        class_Str = class_url + str(num) + ".htm"
        Page_Lis.append(class_Str)
    return Page_Lis


def get_seed_Lis(Page_url,class_Url_True):
    #获取1个page的html
    html = get_Html(Page_url)
    html = html.decode("utf-8")
    #提取一个page中不同seed的url数字正则
    pat = r'htm/pic[0-9]/(\d+)'
    re_urlNum = re.compile(pat,re.S)
    num_List = re_urlNum.findall(html)
    #print(num_List)
    #构造可直接爬取的网页
    #print(class_url)
    seed_Lis = []
    for num in num_List:
        seed_Lis.append(class_Url_True + num + ".htm")
        #print(seed_Lis)
        #print(type(seed_Lis))

    return seed_Lis


def get_Pic(last_Seed_Lis,toPath_Pic):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
    req = urllib.request.Request(last_Seed_Lis, headers=headers)
    response = urllib.request.urlopen(req)
    htmlStr = response.read().decode("utf-8")
    #图片正则表达式
    pat = r';" src="(.+?)">'
    re_image = re.compile(pat, re.S)
    Pic_Lis = re_image.findall(htmlStr)
    #print(Pic_Lis)
    #print(len(Pic_Lis))
    #命名
    for Pic in Pic_Lis:
        global Pic_num
        absPath = os.path.join(toPath_Pic, str(Pic_num) + ".jpg")
        Pic_num += 1
        print(Pic)
        # 下载图片
        # urllib.request.urlretrieve(imageUrl,filename=absPath)
        res = requests.get(Pic)
        with open(absPath , 'wb') as f:
            f.write(res.content)

if __name__ == "__main__":

    toPath_Html_class1 = r"D:\PYUser\爬虫练习\练习4：特殊网站初级爬虫\html\class1.txt"
    toPath_Pic = r"D:\PYUser\爬虫练习\练习4：特殊网站初级爬虫\pic"
    url = r"http://www.721pa.com/"
    class_Lis_num = 0

    #get_Html(url)
    class_Lis,class_Lis_True = get_Class_Lis(url)   #piclist1....9
    print("此Home中class一共有(2级网页)：".center(70," "))
    print(" ".join(class_Lis))

    for class_url in class_Lis:
        Page_Lis = get_Page_Lis(class_url)#分解class成Page
        print("此class中Page一共有(3级网页)：".center(70," "))
        print(" ".join(Page_Lis))

        for Page_url in Page_Lis:
            print("爬取此class中这个Page：".center(70," "))
            print(" ".join(Page_url))
            class_Url_True = class_Lis_True[class_Lis_num]
            print(class_Lis_num , class_Url_True)
            seed_Lis = get_seed_Lis(Page_url,class_Url_True)
            print(" ".join(seed_Lis))

            for seed_url in seed_Lis:
                print("爬取此Page中这个seed(4级网页):".center(70," "))
                print(" ".join(seed_url))
                print("in".center(70," "))
                get_Pic(seed_url,toPath_Pic)
                print("out".center(70," "))
        class_Lis_num += 1
        print("class_Lis_num + 1")
        #3166