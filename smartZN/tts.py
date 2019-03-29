from aip import AipSpeech
from time import sleep
import minimu
from mutagen.mp3 import MP3


def YuyinHecheng(text):
    """ 语音合成"""
    APP_ID = '15565043'
    API_KEY = '3zUBkF64ufjKPATo2HIeEcWd'
    SECRET_KEY = 'p049L8fF0NZxcSqflEWG7ax2G1y2ha0e'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = client.synthesis(text, 'zh', 1, {
        'vol': 5,
        'per':4,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)
    
            
def play():
    # MP3播放
    song=minimu.load('audio.mp3')
    v = MP3('audio.mp3')
    time = v.info.length
    song.play() # 开始播放
    sleep(time)
    song.stop() # 停止播放


def  Synthesizer_Play (text):
    YuyinHecheng(text)
    play()
    print('AI回复:'+text)


