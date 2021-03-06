import pyaudio
import wave
# input_filename = "input.wav"               # 麦克风采集的语音输入
# input_filepath = "G:/baiduspeech/"              # 输入文件的path
# in_path = input_filepath + input_filename

def get_audio():
    # aa = str(input("是否开始录音？   （y/n）"))
    aa = 'y'
    if aa == str("y") :
        CHUNK = 256
        FORMAT = pyaudio.paInt16
        CHANNELS = 1                # 声道数
        RATE = 16000                # 采样率
        RECORD_SECONDS = 3
        WAVE_OUTPUT_FILENAME = 'input.wav'
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("*"*10, "开始录音：请在3秒内输入语音")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("*"*10, "录音结束")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
    elif aa == str("n"):
        try:
            exit()
        except Exception  :
            return 0
    else:
        print("无效输入，请重新选择")
        get_audio()

# 联合上一篇博客代码使用，就注释掉下面，单独使用就不注释
# get_audio(in_path)
