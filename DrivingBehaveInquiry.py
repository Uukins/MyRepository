import csv
import os
from time import time as t
from dateutil.parser import parse

first = ['vehicleplatenumber', 'device_num', 'direction_angle', 'lng', 'lat', 'acc_state', 'right_turn_signals', 'left_turn_signals', 'hand_brake', 'foot_brake', 'location_time', 'gps_speed', 'mileage']

dir = 'D:/py工程/第七届泰迪杯赛题C题-全部数据/附件1-全部数据-450辆车'

class combine():
    def find_file(self,file_dir):  
        for root,dirs,files in os.walk(file_dir):
            return files

    def Write_into_excel(self):
        # 插入首行字段
        with open('车辆数据合并表格.csv','w',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(first)
                print('首行插入成功!')      
        # 插入内容
        filenames = self.find_file(dir)
        for filename in filenames:
            print('表格%s合并中...' % filename)
            file_path = dir+'/'+filename
            with open(file_path) as f:
                datas = csv.reader(f)
                with open('车辆数据合并表格.csv','a',newline='')as f:
                    writer = csv.writer(f)
                    for data in datas:
                        if data != first:
                            writer.writerow(data)
                    print('表格%s完成' % filename)
        
    def mian(self):
        self.Write_into_excel()




class Risky_Driving_Behave(combine):
    def __init__(self):
        car_num=[]
        for root,dirs,files in os.walk(dir):
            for file in files:
                a = file[:7]
                car_num.append(a)

        self.Car_Num = input('请输入你要查询的车牌号:')
        while True:
            if self.Car_Num not in car_num:
                self.Car_Num = input('车牌号输入错误,请重新输入:')
            else:
                break
        
        self.direction_angle = []
        self.lng_lat = []
        self.acc_state = []
        self.right_turn_signals = []
        self.left_turn_signals = []
        self.hand_brake = []
        self.foot_brake = []
        self.location_time = []
        self.gps_speed = []
        self.mileage = []

        file = self.Car_Num + '.csv'
        with open(file) as f:
            datas = csv.reader(f)
            for data in datas:
                if data != first:
                    self.direction_angle.append(data[2])
                    self.lng_lat.append(data[3:5])
                    self.acc_state.append(int(data[5]))
                    self.right_turn_signals.append(data[6])
                    self.left_turn_signals.append(data[7])
                    self.hand_brake.append(data[8])
                    self.foot_brake.append(data[9])
                    self.location_time.append(data[10])
                    self.gps_speed.append(int(data[11]))
                    self.mileage.append(data[12])
        
        self.Choose_Num()
        
    def Choose_Num(self):
        while True:
            print('*'*15)
            print('  1. 疲劳驾驶')
            print('  2. 急加速 ')
            print('  3. 急减速 ')
            print('  4. 超长怠速')
            print('  5. 熄火滑行')
            print('  6. 超速  ')
            print('  退出请按q ')
            print('*'*15)
            Behave_Num = input('请选择:')
            
            if Behave_Num == '1':
                print('正在查询中...') 
                self.Fatigue()
            elif Behave_Num == '2':
                print('正在查询中...') 
                self.Rapid_Acceleration()
            elif Behave_Num == '3':
                print('正在查询中...') 
                self.Rapid_Deceleration()
            elif Behave_Num == '4':
                print('正在查询中...') 
                self.Overlong_Idle()
            elif Behave_Num == '5':
                print('正在查询中...') 
                self.Neutral_Coast()
            elif Behave_Num == '6':
                print('正在查询中...') 
                self.Over_Speed()
            elif Behave_Num == 'q':
                print('已退出程序')
                break
            else:
                print('输入错误,请重新输入')


    def Fatigue(self):
        t_or_f = 0
        warming = 0
        pt = 0
        dsecondlist = []
        psecondlist = []
        timelist1 = []
        timelist2 = []
        for x in range(len(self.gps_speed)):
            if self.gps_speed[x] != 0:
                dt1 = parse(self.location_time[x])
                dsecondlist.append(dt1)
                if warming == 1:
                    if 1200 > pt :
                        t_or_f = 1
                        timelist2.append(dt1)
                        warming = 0
                    warming = 0
            else:
                if dsecondlist != []:              
                    dt1 = dsecondlist[0]
                    dt2 = parse(self.location_time[x-1])
                    td = (dt2-dt1).total_seconds()
                    if td > 14400: # 疲劳驾驶
                        t_or_f = 1
                        timelist1.append(dt1)
                        timelist2.append(dt2)

                    elif 14400 > td > 10800: # 长时间驾驶报警
                        warming = 1
                        pt1 = parse(self.location_time[x])
                        timelist1.append(pt1)
                        psecondlist.append(pt1)
                        pt2 = parse(self.location_time[x])
                        pt = (pt2-psecondlist[0]).total_seconds()

                    dsecondlist = []
                    psecondlist = []
                        
        if t_or_f == 1:
            print('该车辆有疲劳驾驶行为\n时间分别为:')
            for x in range(len(timelist1)):
                print('%s  ----  %s' % (timelist1[x],timelist2[x]))
        else:
            print('该车辆没有疲劳驾驶行为')

            

                       
                   
                
   

    
    def Rapid_Acceleration(self):
        timelist = []
        t_or_f = 0
        for x in range(len(self.gps_speed)):
            v = self.gps_speed[x] - self.gps_speed[x-1]
            t1 = parse(self.location_time[x])
            t2 = parse(self.location_time[x-1])
            t = (t1-t2).total_seconds()
            if v != 0 and t != 0:
                if v // t >= 15:
                    t_or_f = 1
                    timelist.append(t2)
        if t_or_f == 1:
            print('该车辆有急加速行为\n时间分别为:')
            for t in timelist:
                print(t)
        else:
            print('该车没有急加速行为')
                
    
    def Rapid_Deceleration(self):
        timelist = []
        t_or_f = 0
        for x in range(len(self.gps_speed)):
            v = self.gps_speed[x] - self.gps_speed[x-1]
            t1 = parse(self.location_time[x])
            t2 = parse(self.location_time[x-1])
            t = (t1-t2).total_seconds()
            if v != 0 and t != 0:
                if v // t <= -15:
                    t_or_f = 1
                    timelist.append(t2)
        if t_or_f == 1:
            print('该车辆有急减速行为\n时间分别为:')
            for t in timelist:
                print(t)
        else:
            print('该车没有急减速行为')

    def Overlong_Idle(self):
        xlist = []
        secondlist = []
        timelist1 = []
        timelist2 = []
        t_or_f = 0
        for x in range(len(self.acc_state)):
            if self.acc_state[x] == 1 and self.gps_speed[x] == 0:
                t1 = parse(self.location_time[x])
                xlist.append(x)
                secondlist.append(t1)
            else:
                if secondlist != []:              
                    t1 = secondlist[0]
                    t2 = parse(self.location_time[x-1])
                    t = (t2-t1).total_seconds()
                    if t >= 600 :
                        if self.mileage[xlist[0]] == self.mileage[xlist[-1]]:
                            t_or_f = 1
                            timelist1.append(t1)  
                            timelist2.append(t2)  
                            xlist = []
                            secondlist = []                
                    xlist = []
                    secondlist = []
                
        if t_or_f == 1:
            print('该车辆有超长怠速行为\n时间分别是:')
            for x in range(len(timelist1)):
                print('%s  ----  %s' % (timelist1[x],timelist2[x]))
        else:
            print('该车辆没有超长怠速行为')
    
    def Neutral_Coast(self):
        xlist = []
        t_or_f = 0
        for x in range(len(self.acc_state)):
            if self.acc_state[x] == 0 and self.gps_speed[x] > 0:
                t_or_f = 1
                xlist.append(x)
        if t_or_f == 1:
            print('该车辆有熄火滑行行为\n时间分别是:')
            for x in xlist:
                print(self.location_time[x])
        else:
            print('该车辆没有熄火滑行行为')

    
    def Over_Speed(self):
        xlist = []
        t_or_f =0
        for x in range(len(self.gps_speed)):
            if self.gps_speed[x] >= 40:
                t_or_f = 1
                xlist.append(x)
        if t_or_f == 1:
            print('该车辆有超速行为\n时间分别为:')
            for x in xlist:
                print(self.location_time[x])
        else:
            print('该车辆没有超速行为')

    
    

    

if __name__ == "__main__":
   app = Risky_Driving_Behave()
  
   
     
    





