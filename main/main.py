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



    def fingerContrast(self):
        import os
        path = "fingerDataBase/"
        file_list = os.listdir(path)
        for file in file_list:
            img1 = cv2.imread('temp/new.jpg')
            BasePath="fingerDataBase/" + str(file)
            print("BasePath: ", BasePath)
            img2 = cv2.imread(BasePath)
            print("img2: ",img2)
            indexParams = dict(algorithm=0, trees=10)
            searchParams = dict(checks=50)
            flann = cv2.FlannBasedMatcher(indexParams, searchParams)
            matches = flann.knnMatch(des1, des2, k=2)
            matches = sorted(matches, key=lambda x: x[0].distance)

            # 去除错误匹配，0.5是系数，系数大小不同，匹配的结果页不同
            goodMatches = []
            for m, n in matches:
                if m.distance < 0.2 * n.distance:
                    goodMatches.append(m)

            # 获取某个点的坐标位置
            index = int(len(goodMatches) / 2)  # index是获取匹配结果的中位数
            print("index", index)

            if index > 0:
                x, y = kp1[goodMatches[index].queryIdx].pt  # queryIdx是目标图像的描述符索引

                print("file:",file)
                self.textEdit.setPlainText("匹配系数：0.2")
                self.textEdit_2.setPlainText("匹配成功名称："+file)
                print("n: ",n)

                height, width, pixels = img2.shape
                if width > (self.label.width()):
                    rheight = (self.label.width() * height) * width
                    rwidth = self.label.width()
                    print("rwidth-if,rheight-if", width, rheight)
                elif height > (self.label.height()):
                    rwidth = (self.label.height() * width) / height
                    rheight = self.label.height()
                    print("rwidth-elif,rheight-elfi", rwidth, rheight)
                elif ((self.label.height()) - height) < ((self.label.width()) - width):
                    rwidth = (self.label.height() * width) / height
                    rheight = self.label.height()
                    print("rwidth-elif,rheight-elfi", rwidth, rheight)
                else:
                    print("rheight,rwidth", height, width)
                    rheight = height
                    rwidth = width

                frame = cv2.resize(img2, (int(rwidth), int(rheight)))
                print("rwidth-elif,rheight-elfi", rwidth, rheight)
                img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
                _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                                      QtGui.QImage.Format_RGB888)
                jpg_out = QtGui.QPixmap(_image).scaled(rwidth, rheight)  # 设置图片大小
                self.label_2.setPixmap(jpg_out)  # 设置图片显示
                break
            else:
                print("n: ", n)
                self.textEdit.setPlainText("匹配不通过")
                self.textEdit_2.setPlainText(" ")
                self.label_2.setPixmap(QPixmap(""))


if __name__=="__main__":

    app=QtWidgets.QApplication(sys.argv)
    Widget=myWin()
    Widget.showMaximized();
    Widget.show()
    sys.exit(app.exec_())