import itchat

usageMsg = u"1.查询数据          \n" \
           u"2.查询天气          \n" \
           u"3.窗户状态          \n" \
           u"4.当前模式            "

def dates():
    with open('wechat_post.txt','r')as f:
        s = f.readlines()

    date = s[0]+s[1]
    weather = s[2]
    window = s[3]
    state = s[4]
    # print(date)
    return date,weather,window,state


@itchat.msg_register('Text')
def text_reply(msg):
    message = msg['Text']
    # fromName = msg['FromUserName']
    toName = msg['ToUserName']
    date, weather, window, state = dates()
    if toName == "filehelper":
        if message == "1":
            itchat.send(date, 'filehelper')
        if message == "2":
            itchat.send(weather, 'filehelper')
        if message == "3":
            itchat.send(window, "filehelper")
        if message == "4":
            itchat.send(state, "filehelper")
        if message== "手动":
            with open('wechat_order.txt', 'w')as f:
                f.write('A')
        if message == "自动":
            with open('wechat_order.txt', 'w')as f:
                f.write('B')
        if message == "开窗":
            with open('wechat_order.txt', 'w')as f:
                f.write('C')
        if message == "关窗":
            with open('wechat_order.txt', 'w')as f:
                f.write('D')



def wechat_post():
    itchat.auto_login(hotReload=True)
    itchat.send(usageMsg, "filehelper")
    itchat.run()


