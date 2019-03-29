from datetime import datetime


def gettime():
    time = datetime.now().strftime('%H:%M')
    print('现在时间:'+time)
    return '现在的时间是'+time

def getdays():
    day = datetime.now().strftime('%m-%d')
    print(day)
    return '今天的日期是'+day
