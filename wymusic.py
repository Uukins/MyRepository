# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 19:45:13 2019

@author: One
"""
# 617571928
import requests 
from  lxml import etree
import json
import re
from urllib.parse import urlencode

class wangyispider():
    def __init__(self):
        self.url= 'http://music.163.com/api/search/get/web?csrf_token='
        self.headers={"User-Agent":"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
    }
        

    def getpage(self,params):
        res = requests.get(self.url,params,headers = self.headers)
        res.encoding='utf-8'
        html=res.text
#        self.parsepage(html)
        js = json.loads(html)
        id = js['result']['songs'][0]['id']
        params2 = 'os=pc&id='+str(id)+'&lv=-1&kv=-1&tv=-1'
        self.getpage2(id,params2)
        self.comment(id)
        
    def getpage2(self,id,parmas2):
        url = 'http://music.163.com/api/song/lyric?'
        res = requests.get(url,parmas2,headers = self.headers)
        res.encoding='utf-8'
        html=res.text
        js = json.loads(html)
        lyric = js['lrc']['lyric']       
        l = lyric.split('\n')
        for x in l: 
            if x :              
                ric = re.findall(r'\[.*\](.*)',x)               
                print(ric[0])
    
    def comment(self,id):
        # params3='limit='+limit+'&offset='+offset
        url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_'+str(id) #+'?'+urlencode(params3)
        res = requests.get(url,headers = self.headers)
        res.encoding='utf-8'
        html=res.text
        js = json.loads(html)
        n = 0
        for x in js['hotComments']:
            user='昵称：'+x['user']['nickname']+'    用户ID：'+str(x['user']['userId'])
            comment = '评论：'+x['content']
            print('*'*20)
            print(user)
            print(comment)
            n += 1
        print(n)
        

        
        
    def main(self):
        key = input('歌名：')  
           
        params = 'hlpretag=&hlposttag=&s='+key+'&type=1&offset=0&total=true&limit=1'
        self.getpage(params)
        
        
        

if __name__=='__main__':
    app = wangyispider()
    app.main()