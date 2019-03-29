# -*- coding: utf-8 -*-
from urllib import request
import urllib
import sys 
import re  
from  pypinyin  import pinyin
import unicodedata



city_info=request.urlopen( 'http://pv.sohu.com/cityjson').read() 
print(city_info) 
addr =re.findall('"cname": "(.*)"}',city_info.decode('gbk'))
# print(addr)  #输出结构
# print(''.join(addr))

provice = re.findall('(.*)省',addr[0])
city = re.findall('省(.*)市',addr[0])
# print(provice[0])
# print(city[0])

pinyin_provice = pinyin(provice[0])
pinyin_city = pinyin(city[0])
p1 = pinyin_provice[0][0]+pinyin_provice[1][0]
p2 = pinyin_city[0][0]+pinyin_city[1][0]
sheng = unicodedata.normalize('NFKD', p1).encode('ascii','ignore').decode()
shi = unicodedata.normalize('NFKD', p2).encode('ascii','ignore').decode()



url='http://qq.ip138.com/weather/%s/%s.htm'%(sheng,shi)  
# #分析url可知某省某市的天气url即为上面格式  
getdata=request.urlopen(url).read().decode('gbk')
# print(getdata)
# open('天气.txt','w').write(getdata)
tianqi_pattern='alt="(.+?)"'  
tianqi=re.findall(tianqi_pattern, getdata)  #获取天气信息  
  
wendu_pattern='<td>([-]?\d{1,2}.+)</td>'  
wendu=re.findall(wendu_pattern, getdata)  #获取温度信息  
  
# wind_pattern='<td>(\W+\d{1,2}.+)</td>'  
# wind=re.findall(wind_pattern, wea_info)   #获取风向信息  
  
# print('位置：',addr) 
# print('天气：',tianqi[0]) #当天天气，明天天气即为tianqi[1],最多获取6天天气)  
# print('温度：',wendu[0])   #当天温度)
# print('风向：',wind[0])  #当天风向  
# print(tianqi[0]+'    '+wendu[0])