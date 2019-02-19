from PyQt5 import QtCore
import spider

class WorkThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)

    def __int__(self):
        super(WorkThread, self).__init__()

    def run(self):
        self.trigger.emit("Fu*k PyQt5 ".center(70, "*"))

        toPath_Pic = r"D:\PYUser\爬虫练习\练习4：特殊网站初级爬虫\pic" # self.lineEdit.text()
        url = r"http://www.721pa.com/" # self.lineEdit_2.text()
        class_Lis_num = 0


        class_Lis, class_Lis_True = spider.get_Class_Lis(url)  # piclist1....9
        self.trigger.emit("\n此Home中class一共有(2级网页)：\n")
        self.trigger.emit(" ".join(class_Lis))

        for class_url in class_Lis:
            Page_Lis = spider.get_Page_Lis(class_url)  # 分解class成Page
            self.trigger.emit("\n此class中Page一共有(3级网页)：\n")
            self.trigger.emit(" ".join(Page_Lis))

            for Page_url in Page_Lis:
                self.trigger.emit("\n爬取此class中这个Page：\n")
                self.trigger.emit(" ".join(Page_url))
                class_Url_True = class_Lis_True[class_Lis_num]
                # self.trigger.emit(class_Lis_num, class_Url_True)
                seed_Lis = spider.get_seed_Lis(Page_url, class_Url_True)
                self.trigger.emit(" ".join(seed_Lis))

                for seed_url in seed_Lis:
                    self.trigger.emit("\n爬取此Page中这个seed(4级网页): \n")
                    self.trigger.emit(" ".join(seed_url))
                    self.trigger.emit("in".center(60," "))
                    spider.get_Pic(seed_url, toPath_Pic)
                    self.trigger.emit("out".center(60," "))
            class_Lis_num += 1

