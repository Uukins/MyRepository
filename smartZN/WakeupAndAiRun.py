from wakeup import sphinx
from tts import Synthesizer_Play
from AIresponse import Response


def WakeupAndRun():
        callback = sphinx() # 返回实时识别结果
        if callback == 'wakeup':
            ask = '唤醒'
            text = Response(ask)
            Synthesizer_Play(text)
            return 1
        else:
            return 0

# WakeupAndRun()