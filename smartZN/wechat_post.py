import itchat

usageMsg = u"    1.查询室内数据          \n" \
           u"    2.查询当前天气          \n" \
           u"    3.查看窗户状态          \n" \
           u"    4.查看当前模式         \n" \
           u"    5.切换手动模式          \n" \
           u"    6.切换自动模式          \n" \
           u"    7.打开窗户          \n" \
           u"    8.关闭窗户          \n" \



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
        if message== "5":
            with open('wechat_order.txt', 'w')as f:
                f.write('A')
        if message == "6":
            with open('wechat_order.txt', 'w')as f:
                f.write('B')
        if message == "7":
            with open('wechat_order.txt', 'w')as f:
                f.write('C')
        if message == "8":
            with open('wechat_order.txt', 'w')as f:
                f.write('D')



def wechat_post():
    itchat.auto_login(hotReload=True)
    itchat.send(usageMsg, "filehelper")
    itchat.run()


