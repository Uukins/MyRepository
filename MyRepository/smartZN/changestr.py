'''
去掉末尾符号
'''
def changestr(data):
    if type(data) is str:
        c = list(data)
        l = []
        for x in range(len(c)-1):
            l.append(c[x])
        tx = ''.join(l)
        return tx
    else:
        return 'No'