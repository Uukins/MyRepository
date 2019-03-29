
from serial import Serial
from base64 import b64decode
from os import path,mkdir
import matplotlib.pyplot as plt
from datetime import datetime
from pymysql import connect


from ctypes import windll
from configparser import ConfigParser

from serial.tools.list_ports import comports
from PyQt5.QtGui import QIcon
from PyQt5.Qt import Qt
from PyQt5.QtCore import QTimer, QPoint
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget,QRadioButton


from ImgBase64 import close_first as close_first
from ImgBase64 import close_latter as close_latter
from ImgBase64 import maximize_first as maximize_first
from ImgBase64 import maximize_latter as maximize_latter
from ImgBase64 import normal_first as normal_first
from ImgBase64 import normal_latter as normal_latter
from ImgBase64 import minimize_first as minimize_first
from ImgBase64 import minimize_latter as minimize_latter
from ImgBase64 import title_icon as title_icon
from ImgBase64 import icon as icon
from Smart_UI import Ui_Form


from urllib import request

from sys import argv,exit
from re import findall,split
from  pypinyin  import pinyin
from unicodedata import normalize

from AISpeech import AISpeech
from threading import Thread
from WakeupAndAiRun import WakeupAndRun
from tts import Synthesizer_Play
from getdate import getdays,gettime
from wechat_post import wechat_post


def CreateDocument(docPack):
    isExist = path.exists(docPack)
    if not isExist:     # 不存在该文件夹
        mkdir(docPack)       # 创建文件夹


        # win32api.SetFileAttributes(docPack, win32con.FILE_ATTRIBUTE_HIDDEN)  # 隐藏文件夹

        # 从指定目录下加载图片
        LoadImg('D:/SmartImages/close_first.png', close_first)
        LoadImg('D:/SmartImages/close_latter.png', close_latter)
        LoadImg('D:/SmartImages/maximize_first.png', maximize_first)
        LoadImg('D:/SmartImages/maximize_latter.png', maximize_latter)
        LoadImg('D:/SmartImages/normal_first.png', normal_first)
        LoadImg('D:/SmartImages/normal_latter.png', normal_latter)
        LoadImg('D:/SmartImages/minimize_first.png', minimize_first)
        LoadImg('D:/SmartImages/minimize_latter.png', minimize_latter)
        LoadImg('D:/SmartImages/title_icon.ico', title_icon)
        LoadImg('D:/SmartImages/icon.ico', icon)     # 这个图片格式必须为.ico格式，否则无法显示
        print('文件夹创建成功')
    else:       # 如果已经存在文件夹，只需在该文件夹下加载必要的图片
        # 以下操作主要防止用户不小心删除相关文件
        if not path.exists('D:/SmartImages/close_first.png'):
            LoadImg('D:/SmartImages/close_first.png', close_first)

        if not path.exists('D:/SmartImages/close_latter.png'):
            LoadImg('D:/SmartImages/close_latter.png', close_latter)

        if not path.exists('D:/SmartImages/maximize_first.png'):
            LoadImg('D:/SmartImages/maximize_first.png', maximize_first)

        if not path.exists('D:/SmartImages/maximize_latter.png'):
            LoadImg('D:/SmartImages/maximize_latter.png', maximize_latter)

        if not path.exists('D:/SmartImages/normal_first.png'):
            LoadImg('D:/SmartImages/normal_first.png', normal_first)

        if not path.exists('D:/SmartImages/normal_latter.png'):
            LoadImg('D:/SmartImages/normal_latter.png', normal_latter)

        if not path.exists('D:/SmartImages/minimize_first.png'):
            LoadImg('D:/SmartImages/minimize_first.png', minimize_first)

        if not path.exists('D:/SmartImages/minimize_latter.png'):
            LoadImg('D:/SmartImages/minimize_latter.png', minimize_latter)

        if not path.exists('D:/SmartImages/title_icon.ico'):
            LoadImg('D:/SmartImages/title_icon.ico', title_icon)

        if not path.exists('D:/SmartImages/icon.ico'):
            LoadImg('D:/SmartImages/icon.ico', icon)
        print('图片加载完成')
        return None

def LoadImg(picPath, name):
    tmp = open(picPath, 'wb+')  # 在指定目录下创建文件
    tmp.write(b64decode(name))  # 解码图片
    tmp.close()  # 关闭写

class Smart(QWidget,Ui_Form):
    a = True
    def __init__(self,parent=None):
        super(Smart,self).__init__(parent)
        CreateDocument('D:/SmartImages')
        self.setupUi(self)  # 初始化界面
        self.InitSetting()  # 初始化配置/加载上一次使用的数据
        self.MoveCenter()       # 将窗口移到屏幕中间


        windll.shell32.SetCurrentProcessExplicitAppUserModelID('myappid')  # 主要是解决Windows任务栏下无法显示图标的问题
        self.setWindowIcon(QIcon('D:\SmartImages\icon.ico'))  # 设置标题栏、任务栏等的图标

        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinimizeButtonHint)  # 隐藏标题栏，支持右键菜单，允许最小化还原
        self.setAttribute(Qt.WA_TranslucentBackground)


        self.padding = 4  # 设置边界宽度为5，用于边缘拉伸

        # 窗口移动及拉伸的状态位
        self.move_drag = False  # 移动状态
        self.move_drag_position = 0  # 移动距离变量
        self.corner_drag = False  # 右下角拉伸状态
        self.corner_rect = 0  # 右下角拉伸位置变量
        self.right_drag = False  # 右侧拉伸状态
        self.right_rect = 0  # 右侧拉伸位置变量
        self.bottom_drag = False  # 下方拉伸状态
        self.bottom_rect = 0  # 下方拉伸位置变量



        self.ser =Serial()              # 实例化串口
        self.timer_receive = QTimer(self)  # 实例化接收定时器

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.Operate)

        self.RefreshCOM()  # 刷新串口列表
        # self.timer_refresh = QTimer(self)  # 初始化定时器
        # self.timer_refresh.setInterval(5000)  # 设置定时器时间为2.5s
        # self.timer_refresh.start()  # 开启串口刷新定时器
        # self.timer_refresh.timeout.connect(self.RefreshCOM)  # 定时刷新串口列表

        # 定时插入数据库
        self.mysql_refresh = QTimer(self)
        self.mysql_refresh.setInterval(3600000) #1hour
        self.mysql_refresh.start()
        self.mysql_refresh.timeout.connect(self.OpenMysql)
        #按键插入数据库
        self.postsql.clicked.connect(self.OpenMysql)

        self.OpenButton.clicked.connect(self.OpenOrCloseSerial)
        self.change.clicked.connect(self.State_Change)
        self.order_change.clicked.connect(self.Order_Change)
        self.timer_receive.setInterval(100)
        self.timer_receive.start()
        self.timer_receive.timeout.connect(self.Show_Data)  # 定时接收

        self.Analysisbutton.clicked.connect(self.Analysis)

        self.Show_Data()

        self.ReceiveData()

        self.getyoutips()
        self.refresh.clicked.connect(self.getyoutips)

        self.yuyinzhushou.clicked.connect(self.wake_run)
        self.AIrun()


        # self.wechat_listen.toggled.connect(self.choose_btn)


        # 初始化查询数据库时间选择框
        time = datetime.now().strftime('%Y-%m-%d')
        t = split('-', time)
        self.years.setCurrentText(t[0])
        self.months.setCurrentText(t[1])
        self.days.setCurrentText(t[2])

    def InitSetting(self):
        global config
        if not path.exists('setting.ini'):  # 检测是否存在配置文件
            open('setting.ini', 'w')  # 创建配置文件

        config = ConfigParser()  # 加载现有配置文件
        config.read('setting.ini')  # 读取ini文件

        if not config.has_section('globals'):  # 如果为空
            config['globals'] = {'baudrate': '9600'}  # 向配置文件写入数据
            with open('setting.ini', 'w') as configfile:  # with用法，先打开数据再写
                config.write(configfile)
        # 把配置文件的数据加载到窗口
        self.SerialBaudRateComboBox.setCurrentText(config.get('globals', 'baudrate'))




    def resizeEvent(self, QResizeEvent):        # 当窗口大小发生变化时，边框的位置需要重新计算，为边缘拉伸做准备
        try:
            self.corner_rect = [QPoint(x, y) for x in range(self.width() - self.padding, self.width() + 1)
                                for y in range(self.height() - self.padding, self.height() + 1)]

            self.right_rect = [QPoint(x, y) for x in range(self.width() - self.padding, self.width() + 1)
                               for y in range(1, self.height() - self.padding)]

            self.bottom_rect = [QPoint(x, y) for x in range(1, self.width() - self.padding)
                                for y in range(self.height() - self.padding, self.height() + 1)]
        except Exception as e:
            print(e)

    def mousePressEvent(self, event):  # 鼠标点击时间
        if (event.button() == Qt.LeftButton) and (event.y() < self.TitleBar.height()):  # 鼠标点击在标题栏位置
            self.move_drag = True
            self.move_drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        # 这里主要设置鼠标放在特定位置时鼠标的图标发生变化
        if QMouseEvent.pos() in self.corner_rect:
            self.setCursor(Qt.SizeFDiagCursor)

        elif QMouseEvent.pos() in self.right_rect:
            self.setCursor(Qt.SizeHorCursor)

        elif QMouseEvent.pos() in self.bottom_rect:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        # 这里就是实现拉伸、拖拽
        if Qt.LeftButton and self.corner_drag:
            self.resize(QMouseEvent.pos().x(), QMouseEvent.pos().y())  # 窗口移动的位置
            QMouseEvent.accept()

        elif Qt.LeftButton and self.right_drag:
            self.resize(QMouseEvent.pos().x(), self.height())
            QMouseEvent.accept()

        elif Qt.LeftButton and self.bottom_drag:
            self.resize(self.width(), QMouseEvent.pos().y())
            QMouseEvent.accept()

        elif Qt.LeftButton and self.move_drag:
            self.move(QMouseEvent.globalPos() - self.move_drag_position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标松开，复位所有状态位
        self.corner_drag = False
        self.right_drag = False
        self.bottom_drag = False
        self.move_drag = False

    def MoveCenter(self):  # 将窗口移动到中间，备用
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    @QtCore.pyqtSlot()
    def on_MinimizeButton_clicked(self):  # 最小化窗口
        try:
            self.showMinimized()
        except Exception as e:
            print(e)

    @QtCore.pyqtSlot()
    def on_CloseButton_clicked(self):
        """
        关闭窗口
        """
        try:
            if self.ser.is_open:
                self.ser.write('B'.encode())  # 重置电机为自动状态
                self.timer_receive.stop()
                self.close()
            else:
                self.timer_receive.stop()
                self.close()
        except Exception as e :
            print(e)

    # @QtCore.pyqtSlot()
    # def on_exit_clicked(self):
    #     """
    #     关闭窗口
    #     """
    #     try:
    #         if self.ser.is_open:
    #             self.ser.write('B'.encode())  # 重置电机为自动状态
    #             self.timer_receive.stop()
    #
    #         else:
    #
    #             self.timer_receive.stop()
    #             self.close()
    #
    #     except Exception as e:
    #         print(e)


    def State_Change(self):
        self.state = self.show_state.toPlainText()
        if self.state == '   自动模式':
            try:
                self.ser.write('A'.encode())
                print('发送指令成功')
                self.change.setText(u'自动')
                # self.show_state.setPlainText('   手动模式')
                print('手动模式开始')
                if self.show_state_2.toPlainText() == '    打开':
                    self.order_change.setText(u'关闭')
                else:
                    self.order_change.setText(u'打开')

            except Exception as e:
                QMessageBox.critical(self, '警告', '请打开串口')
                print(e)
        else:
            try:
                self.ser.write('B'.encode())
                print('发送指令成功')
                self.change.setText(u'手动')
                # self.show_state.setPlainText('   自动模式')
                if self.show_state_2.toPlainText() == '    打开':
                    self.order_change.setText(u'关闭')
                else:
                    self.order_change.setText(u'打开')

                print('自动模式开始')
            except Exception as e:
                QMessageBox.critical(self, '警告', '请打开串口')
                print(e)

    def Order_Change(self):
        self.state1 = self.show_state_2.toPlainText() # 当前状态
        self.state2 = self.state = self.show_state.toPlainText()# 当前模式
        try:
            if self.state2 == '   自动模式':
                QMessageBox.critical(self, '警告', '请打开串口并切换手动模式')
            # elif self.state1 =='':
            #     self.ser.write('C'.encode())
            #     print('正在打开')
            #     self.order_change.setText(u'关闭')
                # self.timer.start(10000)  # 10s
                self.show_state_2.setPlainText('正在打开...')
            elif self.state1 == '    打开':
                self.ser.write('D'.encode())
                print('正在关闭')
                self.order_change.setText(u'打开')
                # self.timer.start(10000)  # 5S
                self.show_state_2.setPlainText('正在关闭...')
            elif self.state1== '    关闭':
                self.ser.write('C'.encode())
                print('正在打开')
                self.order_change.setText(u'关闭')
                # self.timer.start(10000)  # 5S
                self.show_state_2.setPlainText('正在打开...')

        except Exception as e:
            QMessageBox.critical(self, '警告', 'error')
            print(e)

    def wechat_order(self):
        with open('wechat_order.txt', 'r')as f:
            orders = f.read()
            if orders == "A":
                self.ser.write('A'.encode())
                with open('wechat_order.txt', 'w')as f:
                    f.write('')
            if orders == "B":
                self.ser.write('B'.encode())
                with open('wechat_order.txt', 'w')as f:
                    f.write('')
            if orders == "C":
                self.ser.write('C'.encode())
                with open('wechat_order.txt', 'w')as f:
                    f.write('')
            if orders == "D":
                self.ser.write('D'.encode())
                with open('wechat_order.txt', 'w')as f:
                    f.write('')


    def Show_Data(self):
        try:
            shijian = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.show_time.setText(shijian)
            if self.ser.is_open:
                receive_bytes_num = self.ser.inWaiting()
                if receive_bytes_num > 0:
                    data = self.ser.read(receive_bytes_num)
                    a = data.decode()
                    if a != 'a':
                        s = 'a' + a
                        l = split('a=', s)[1:]
                        if len(l) == 4 and len(l[3]) == 2:
                            self.p1 = l[0] # 温度
                            self.p2 = l[1] # 光照
                            self.p3 = l[2] # 模式
                            self.p4 = l[3] # 状态
                            self.show_temp.setPlainText(self.p1+'℃')
                            self.show_light.setPlainText(self.p2+'cd')
                            if self.p3 == 'ON':
                                window = '打开'
                                self.show_state_2.setPlainText('    打开')
                            elif self.p3 == 'OF':
                                window = '关闭'
                                self.show_state_2.setPlainText('    关闭')
                            if self.p4 == 'AU':
                                state = '自动模式'
                                self.show_state.setPlainText('   自动模式')
                            elif self.p4 == 'HD':
                                state = '手动模式'
                                self.show_state.setPlainText('   手动模式')

                            wechat_text = '温度:' + self.p1 + '℃'+'\n' + '光照:' + self.p2 +'cd'+ '\n' \
                                          + '今天天气' + self.weather + ',温度大概在' +self.wendu_max_min+'\n'+\
                                          '窗户处于'+window+'状态'+'\n'\
                                          +'当前模式:'+state
                            with open('wechat_post.txt', 'w') as f:
                                f.write(wechat_text)
                            self.wechat_order()

        except Exception as e:
            print(e)

    def Analysis(self):
        try:
            temp = []
            light = []
            shifen = []
            s = []
            db = connect('localhost', 'root', '123456', 'bs', charset='utf8', port=3306)
            cur = db.cursor()
            years = self.years.currentText()
            months = self.months.currentText()
            days = self.days.currentText()
            l = years+'-'+months+'-'+days+'%'
            caozuo = 'select 温度,光强,时间 from 传感器数据 where 时间 like ' + '"'+l+'"'
            try:
                cur.execute(caozuo)
                All = cur.fetchall()
                for x in All:
                    temp.append(int(findall('\d*', x[0])[0]))
                    light.append(int(findall('\d*', x[1])[0]))
                    shifen.append(x[2][11:16])
                    a = ' '+x[0]+'   '+x[1]+'   '+x[2][11:16]+'\n'
                    s.append(a)
                b = ''.join(s)
                if b != '':
                    c = ' 温度     光强     时间  \n'+b
                    print(c)
                    print('数据库下载成功')
                    self.show_data.setPlainText(c)
                else:
                    self.show_data.setPlainText('暂无数据...')
            except Exception as e:
                print('下载数据库失败',e)

            cur.close()
            db.close()
            plt.figure(figsize=(14, 7))  # figure大小
            font2 = {'family': 'Times New Roman',
                     'weight': 'normal',
                     'size': 10,
                     }
            ax1 = plt.subplot(2, 1, 1)  # 两行一列第一行
            ax2 = plt.subplot(2, 1, 2)  # 两行一列第二行
            # ax1(温度)
            plt.sca(ax1)
            plt.xlabel('time', font2)
            plt.ylabel('temp/°C', font2)
            plt.plot(shifen, temp, color='red')
            # ax2(光强)
            plt.sca(ax2)
            plt.xlabel('time', font2)
            plt.ylabel('light intensity/cd', font2)
            plt.plot(shifen, light, color='blue')
            # 作图
            plt.show()

            #print(temp,light,shifen)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, '警告', '正在连接...请稍后')



    def RefreshCOM(self):
        port_list = comports()  # 获取所有串口的端口

        if len(port_list) == 0:  # 如果串口列表为0，即没有端口
            self.SerialCOMComboBox.clear()
        else:
            for port, desc, hwid in comports():  # 识别串口
                if self.SerialCOMComboBox.findText(port) != -1:  # 如果combox中已经有该串口，则不需再次添加
                    pass
                else:
                    self.SerialCOMComboBox.addItem(port)  # 把串口号添加到Box

    def on_SerialBaudRateComboBox_activated(self):
        if self.SerialBaudRateComboBox.currentText() == '自定义':
            self.SerialBaudRateComboBox.setEditable(True)  # 打开可编辑功能
        else:
            self.SerialBaudRateComboBox.setEditable(False)  # 关闭可编辑功能

    def OpenOrCloseSerial(self):
        self.ser.port = self.SerialCOMComboBox.currentText()
        try:
            self.ser.baudrate = int(self.SerialBaudRateComboBox.currentText())
        except Exception:
            QMessageBox.critical(self, '警告', '请输入正确的波特率')
            return None
        if not self.ser.is_open:
            try:
                self.ser.open()
                self.ser.write('B'.encode())  # 重置电机为自动状态(预防电机还在手动状态)
                print(self.ser.is_open)
                print('串口已打开 波特率为%s' % self.ser.baudrate,'端口为%s'%self.ser.port)

                self.SerialCOMComboBox.setEnabled(False)  # 关闭串口选择功能

                self.OpenButton.setText(u'关闭串口')

                # self.show_state.setPlainText('   自动模式')

                self.Show_Data()

                # text = '好了,连接完成'  # 为避免重复播报,再此插入播报,取消在wake_run里面播报
                # Synthesizer_Play(text)

            except Exception as e:
                print(e)
                # QMessageBox.critical(self, '警告', '串口不存在或被占用') # AI触发异常会出现冲突卡死,转为语音播报异常
                text = '警告,串口不存在或已被占用'
                Synthesizer_Play(text)
                return None
        else:
            self.change.setText(u'手动')
            # self.show_state.setPlainText('   自动模式')
            self.order_change.setText(u'(打开/关闭)')
            # self.show_state_2.setPlainText('')
            self.ser.write('B'.encode())  # 重置电机为自动状态
            self.ser.close() #关闭串口
            print('串口已关闭')
            self.SerialCOMComboBox.setEnabled(True)  # 关闭串口选择功能
            self.OpenButton.setText(u'打开串口')

    def ReceiveData(self):  # 接收数据
        if self.ser.is_open:  # 是否打开串口
            try:
                self.ser.baudrate = int(self.SerialBaudRateComboBox.currentText())
            except Exception:
                QMessageBox.critical(self, '警告', '请先关闭串口')
                self.ser.close()
                self.OpenButton.setText(u'打开串口')
                return None



    def OpenMysql(self):
        if self.ser.is_open:
            db = connect('localhost', 'root', '123456', 'bs', charset='utf8', port=3306)
            cur = db.cursor()
            shijian = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            wendu = self.p1 + '°C'
            light = self.p2 + 'cd'
            l = [wendu, light, shijian]
            caozuo = 'insert into 传感器数据 values(%s,%s,%s)'
            try:
                cur.execute(caozuo, l)
                db.commit()
                print('插入成功!\n')
                QMessageBox.information(self, '提示', '插入成功!')
            except Exception as e:
                db.rollback()
                print('failed', e)
            cur.close()
            db.close()
        else:
            QMessageBox.critical(self, '警告', '插入失败,请确定串口是否打开!')

    def getyoutips(self):
        try:
            city_info = request.urlopen('http://pv.sohu.com/cityjson').read()
            addr = findall('"cname": "(.*)"}', city_info.decode('gbk'))
            provice = findall('(.*)省', addr[0])
            city = findall('省(.*)市', addr[0])
            pinyin_provice = pinyin(provice[0])
            pinyin_city = pinyin(city[0])
            p1 = pinyin_provice[0][0] + pinyin_provice[1][0]
            p2 = pinyin_city[0][0] + pinyin_city[1][0]
            sheng =normalize('NFKD', p1).encode('ascii', 'ignore').decode()
            shi =normalize('NFKD', p2).encode('ascii', 'ignore').decode()

            url = 'http://qq.ip138.com/weather/%s/%s.htm' % (sheng, shi)
            getdata = request.urlopen(url).read().decode('gbk')

            tianqi_pattern = 'alt="(.+?)"'
            tianqi = findall(tianqi_pattern, getdata)  # 获取天气信息

            wendu_pattern = '<td>([-]?\d{1,2}.+)</td>'
            wendu_max_min = findall(wendu_pattern, getdata)  # 获取温度信息

            self.show_addr.setText(''.join(addr))
            self.show_weather.setText(tianqi[0]+'    '+wendu_max_min[0])
            self.weather = tianqi[0]
            self.wendu_max_min = wendu_max_min[0]
        except Exception :
            self.show_addr.setText('网络未连接上')
            self.show_weather.setText('请重新连接网络')


    def wake_run(self):
        while True:
            if WakeupAndRun() == 1: # 循环识别唤醒并获取返回值
                ask = AISpeech() # 询问并获取指令
                print('终端收到的指令:' + ask)
                if ask in ['连接端口']:
                    if self.ser.is_open:
                        text = '端口已经连接了'
                        Synthesizer_Play(text)
                    else:
                        self.OpenOrCloseSerial()
                        if self.ser.is_open:
                            text = '好了,连接完成'
                            Synthesizer_Play(text)

                if ask in ['断开端口']:
                    if not self.ser.is_open:
                        text = '连接已经断开了'
                        Synthesizer_Play(text)
                    else:
                        self.OpenOrCloseSerial()
                        text = '好了.断开完成'
                        Synthesizer_Play(text)

                if ask in ['切换手动模式']:
                    if self.ser.is_open:
                        if self.show_state.toPlainText() == '   手动模式':
                            text = '现在已经是手动模式了'
                            Synthesizer_Play(text)
                        else:
                            self.ser.write('A'.encode())
                            print('手动模式切换成功')
                            self.change.setText(u'自动')
                            text='手动模式切换成功'
                            Synthesizer_Play(text)
                    else:
                        text = '请先连接主机,再切换手动模式'
                        Synthesizer_Play(text)

                if ask in ['切换自动模式']:
                    if self.ser.is_open:
                        if self.show_state.toPlainText() == '   自动模式':
                            text = '现在已经是自动模式了'
                            Synthesizer_Play(text)
                        else:
                            self.ser.write('B'.encode())
                            print('自动模式切换成功')
                            self.change.setText(u'自动')
                            text='自动模式切换成功'
                            Synthesizer_Play(text)
                    else:
                        text = '请先连接主机,再切换自动模式'
                        Synthesizer_Play(text)

                if ask in ['打开窗户']:
                    if self.show_state.toPlainText() == '   自动模式':
                        text = '请先切换手动模式,再打开窗户'
                        Synthesizer_Play(text)
                    else:
                        if self.show_state_2.toPlainText() == '    打开':
                            text = '窗户已经打开了'
                            Synthesizer_Play(text)
                        else:
                            self.ser.write('C'.encode())
                            print('正在打开')
                            self.order_change.setText(u'关闭')
                            text = '完成窗户打开'
                            Synthesizer_Play(text)

                if ask in ['关闭窗户']:
                    if self.show_state.toPlainText() == '   自动模式':
                        text = '请先切换手动模式,再关闭窗户'
                        Synthesizer_Play(text)
                    else:
                        if self.show_state_2.toPlainText() == '    关闭':
                            text = '窗户已经关闭了'
                            Synthesizer_Play(text)
                        else:
                            self.ser.write('D'.encode())
                            print('正在关闭')
                            self.order_change.setText(u'打开')
                            text = '完成窗户关闭'
                            Synthesizer_Play(text)

                if ask in ['查询天气','天气怎样','今天天气','天气']:
                    text = '今天天气'+self.weather+',温度大概在'+self.wendu_max_min
                    Synthesizer_Play(text)

                if ask in ['查询温度','现在的温度是多少','现在多少度']:
                    text = '现在是'+ self.p1+'摄氏度'
                    Synthesizer_Play(text)

                if ask in [ '现在几点','几点了','查询时间']:
                    text = gettime()
                    Synthesizer_Play(text)

                if ask in ['查询日期','今天几号']:
                    text = getdays()
                    Synthesizer_Play(text)

                if ask in ['退出程序']:
                    if self.ser.is_open:
                        self.ser.write('B'.encode())  # 重置电机为自动状态
                        self.timer_receive.stop()
                        self.close()
                        text = '完成程序退出,moss将在两秒后下线'
                        Synthesizer_Play(text)
                        break
                    else:
                        self.timer_receive.stop()
                        self.close()
                        text = '完成程序退出,moss将在两秒后下线'
                        Synthesizer_Play(text)
                        break
            else:
                continue

    def AIrun(self):
        ai = Thread(target = self.wake_run)
        ai.start()
        wechat = Thread(target = wechat_post)
        wechat.start()


if __name__ == '__main__':
    while True:
        app = QApplication(argv)
        win = Smart()
        win.show()
        exit(app.exec_())


