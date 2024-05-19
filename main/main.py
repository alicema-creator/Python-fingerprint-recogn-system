# coding:utf-8
import sys
#从转换的.py文件内调用类
import cv2
import cv2 as cv
import numpy as np

from PyQt5 import QtWidgets

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class myWin(QtWidgets.QWidget, Ui_Dialog):

    def __init__(self):
        super(myWin, self).__init__()
        self.setupUi(self)

    def openFileButton(self):
        imgName, imgType  = QFileDialog.getOpenFileName(self,"打开文件","./","files(*.*)")
        img = cv2.imread(imgName)
        cv2.imwrite("temp/new.jpg", img)
        height, width, pixels = img.shape
        print("width,height",width,height)
        print("self.label.width()",self.label.width())
        print("self.label.height()",self.label.height())

        if width>(self.label.width()):
            rheight=(self.label.width()*height)*width
            rwidth=self.label.width()
            print("rwidth-if,rheight-if", width, rheight)
        elif height>(self.label.height()):
            rwidth=(self.label.height()*width)/height
            rheight=self.label.height()
            print("rwidth-elif,rheight-elfi", rwidth, rheight)
        elif ((self.label.height())-height)<((self.label.width())-width):
            rwidth=(self.label.height()*width)/height
            rheight=self.label.height()
            print("rwidth-elif,rheight-elfi", rwidth, rheight)
        else:
            print("rheight,rwidth", height, width)
            rheight = height
            rwidth = width

        frame = cv2.resize(img, (int(rwidth), int(rheight)))
        print("rwidth-elif,rheight-elfi", rwidth, rheight)
        img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3, QtGui.QImage.Format_RGB888)
        jpg_out = QtGui.QPixmap(_image).scaled(rwidth, rheight) #设置图片大小
        self.label.setPixmap(jpg_out) #设置图片显示


    def saveFileButton(self):
        img = cv2.imread("temp/new.jpg")
        file_path = QFileDialog.getSaveFileName(self, "save file", "./save/test","jpg files (*.jpg);;all files(*.*)")
        print(file_path[0])
        cv2.imwrite(file_path[0], img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



  

if __name__=="__main__":

    app=QtWidgets.QApplication(sys.argv)
    Widget=myWin()
    Widget.showMaximized();
    Widget.show()
    sys.exit(app.exec_())
