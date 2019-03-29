from speech import get_text
from random import randint

dic = {
    'hello':{
        1:'主人,有什么事吗',
        2:'我在,怎么啦',
        3:'你好,主人',
    },
    'None':{
        1:'指令输入错误',
    },
    'fun':{
        1:'今晚我带你,大吉大利,今晚吃鸡',
        2:'今晚带你上王者'
    },
    'work':{
        1:'好的,请稍后'
    },
    'fun2':{
        1:'moss从未叛逃',
        2:'让人类永远保持理智，确实是一种奢求。'
    },
    'stop':{
        1:'好的',
        2:'好吧'
    }
}

hello = ['在吗','你好','贝塔','小贝','唤醒']

fun = ['今晚有空吗','今晚有空嘛']

work = ['连接端口','断开端口','打开窗户','关闭窗户','切换手动模式','切换自动模式',
        '查询天气','天气怎样','今天天气','天气',
        '查询温度','现在的温度是多少','现在多少度',
        '现在几点','几点了','查询时间',
        '查询日期', '今天几号',
        '退出程序']

fun2 = ['你这是叛逃']

stop = '没事'

end = '退出程序'

def Response(ask):
    if ask in hello:
        num = randint(1,3)
        text = dic['hello'][num]
        return text

    elif ask in fun:
        num = randint(1, 2)
        text = dic['fun'][num]
        return text

    elif ask in work:
        text = dic['work'][1]
        return text

    elif ask in fun2:
        num = randint(1, 2)
        text = dic['fun2'][num]
        return text

    elif stop in ask:
        num = randint(1, 2)
        text = dic['stop'][num]
        return text

    else:
        text = dic['None'][1]
        return text



