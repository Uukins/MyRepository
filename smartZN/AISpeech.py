from get_audio import get_audio
from speech import get_text
from tts import Synthesizer_Play
from AIresponse import Response
from changestr import changestr

'''

语音识别系统

'''

count = 0

def AISpeech():
        global count
        get_audio() # 录音

        data = get_text() # 获取语音识别文本

        ask = changestr(data)# 规范文本内容

        callback = Response(ask) # AI返回语句

        Synthesizer_Play(callback)

        print(count)

        if count < 2:  # 超过两次录入不清晰自动退出
                count += 1
                if callback == '指令输入错误':
                        ask = AISpeech()
        else:
                count = 0
                pass

        return ask
