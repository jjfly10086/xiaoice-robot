import itchat
from itchat.content import *
from queue import Queue


# 微信微软小冰公众号
XIAO_ICE_USER_NAME = ''
# 消息发送者队列
my_queue = Queue()
# 最后一个队列用户，默认我自己
last_to_user_name = '***********************'


# 监听个人文字消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_replay(msg):
    print('receive personal message from [%s], msgType: [%s], message: [%s]' % (msg.fromUserName, msg.type, msg.text))
    # 存队列
    my_queue.put(msg.fromUserName)
    global last_to_user_name
    last_to_user_name = msg.fromUserName
    # 向小冰发送消息
    itchat.send(msg.text, toUserName=XIAO_ICE_USER_NAME)
    # msg.user.send('%s: %s' % (msg.type, msg.text))


# 监听个人附件消息
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print('receive personal message from [%s], msgType: [%s], message: [%s]' % (msg.fromUserName, msg.type, msg.text))
    msg.download(msg.fileName)
    type_symbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    to_msg = '@%s@%s' % (type_symbol, msg.fileName)
    # 存队列
    my_queue.put(msg.fromUserName)
    global last_to_user_name
    last_to_user_name = msg.fromUserName
    # 向小冰发送消息
    itchat.send(to_msg, toUserName=XIAO_ICE_USER_NAME)


# 监听公众号文字消息
# 消息类型，是否是个人消息，群组消息，公众号消息
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isFriendChat=False, isGroupChat=False, isMpChat=True)
def get_message(msg):
    print('receive 公众号消息 from [%s], msgType: [%s], message: [%s]' % (msg.fromUserName, msg.type, msg.text))
    if msg.fromUserName == XIAO_ICE_USER_NAME:
        if my_queue.empty():
            toUserName = last_to_user_name
            print('queue is empty, use last userName: [%s]' % last_to_user_name)
        else:
            toUserName = my_queue.get()
        print('to send userName %s' % toUserName)
        itchat.send(msg.text, toUserName=toUserName)


# 监听公众号媒体消息
# 消息类型，是否是个人消息，群组消息，公众号消息
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=False, isGroupChat=False, isMpChat=True)
def get_message(msg):
    print('receive 公众号消息 from [%s], msgType: [%s], message: [%s]' % (msg.fromUserName, msg.type, msg.text))
    msg.download(msg.fileName)
    if msg.fromUserName == XIAO_ICE_USER_NAME:
        if my_queue.empty():
            toUserName = last_to_user_name
            print('queue is empty, use last userName: [%s]' % last_to_user_name)
        else:
            toUserName = my_queue.get()
        print('to send userName %s' % toUserName)
        type_symbol = {
            PICTURE: 'img',
            VIDEO: 'vid', }.get(msg.type, 'fil')
        to_msg = '@%s@%s' % (type_symbol, msg.fileName)
        itchat.send(to_msg, toUserName=toUserName)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    mps = itchat.search_mps(name='小冰')
    print(mps[0]['UserName'])
    XIAO_ICE_USER_NAME = mps[0]['UserName']
    itchat.run()
   
