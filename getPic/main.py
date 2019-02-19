from untitled import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from time import sleep
import mythread


class MyUI(Ui_MainWindow,QtWidgets.QMainWindow):
    def __init__(self):
        super(MyUI,self).__init__()
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        sleep(1)

        self.pushButton.clicked.connect(self.get_Save_Path)
        self.pushButton_2.clicked.connect(self.get_URL)
        self.pushButton_3.clicked.connect(self.Start)
        self.pushButton_4.clicked.connect(self.About)
        self.pushButton_5.clicked.connect(self.Stop)

    def get_Save_Path(self):
        dir_choose = QFileDialog.getExistingDirectory(self,"File")
        self.lineEdit.setText(dir_choose)
        # self.lineEdit.setClearButtonEnabled(True)
        if dir_choose == "":
            self.textBrowser.append("\n取消选择")
            return
        self.textBrowser.append("\n你选择的文件夹为:")
        self.textBrowser.append(dir_choose)

    def get_URL(self):
        enter_URL = self.lineEdit_2.text()
        self.lineEdit_2.setText(enter_URL)
        if enter_URL == "":
            self.textBrowser.append("\n取消输入")
            return
        self.textBrowser.append("\n你选择的URL为:")
        self.textBrowser.append(enter_URL)

    def Start(self):
        self.workThread = mythread.WorkThread()
        self.workThread.trigger.connect(self.Show)  # 链接你执行完这个线程之后的想要触发的 函数的名字
        self.workThread.start()

    def Show(self,text):
        self.textBrowser.append(text)

    def Stop(self):
        pass

    def About(self):
        My_button = QMessageBox.about(self, "About", u"作者：Richarming\n本软件只供学习之用，请勿用于商业，如有一切后果有自己承担。")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    splash = QSplashScreen(QPixmap(r":/my_pic/Open.png"))
    splash.show()
    app.processEvents()
    ui = MyUI()
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec_())