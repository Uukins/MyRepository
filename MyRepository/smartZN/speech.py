from aip import AipSpeech

""" 你的 APPID AK SK """
APP_ID = '15565043'
API_KEY = '3zUBkF64ufjKPATo2HIeEcWd'
SECRET_KEY = 'p049L8fF0NZxcSqflEWG7ax2G1y2ha0e'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def get_text():
    res = client.asr(get_file_content('input.wav'), 'wav', 16000, {
        'dev_pid': 1537,
    })
    if res['err_no'] == 0:
        print('--->  '+res['result'][0]+'\n')
        return res['result'][0]

    else:
        print('错误代码:'+str(res['err_no']))
        return 'No.'






