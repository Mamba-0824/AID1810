#!/usr/bin/env python3
#coding=utf8
'''
name:  Huang
email: huangqinggu24@163.com
date:  2010-2
class: AID
introduce: Chatroom server
env  : python3.6
'''

from socket import *
import os,sys

# 做管理员喊话
def do_child(s, addr):
    while True:
        msg = input("管理员消息:")
        msg = 'C 管理员 ' + msg
        s.sendto(msg.encode(), addr)

def do_chat(s, user, name, text):
    msg = "\n%s 说:%s" % (name, text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(), user[i])


def do_quit(s, user, name):
    msg = '\n' + name + '退出了聊天室'
    for i in user:
        if i == name:
            s.sendto(b'EXIT', user[i])
                        
        else:
            s.sendto(msg.encode(), user[i])
    del user[name]
        

# 接受客户端请求
def do_parent(s):
    #存储结构｛'zhangsan':('127.0.0.1',9999)｝
    user = {}
    while True:
        msg, addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')

        # 区分请求类型
        if msgList[0] == 'L':
            do_login(s, user, msgList[1], addr)
        elif msgList[0] == 'C':
            do_chat(s, user, msgList[1], ' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            do_quit(s, user, msgList[1])



def do_login(s, user, name, addr):
    if (name in user) or name == '管理员':
        s.sendto('该用户已存在'.encode(), addr)
        return
    s.sendto(b'OK', addr)

    #通知其他人
    msg = "\n欢迎 %s 进入聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])
    user[name] = addr


#创建网络，创建进程，调用功能函数
def main():
    #server address
    ADDR = ('0.0.0.0', 8888)

    #创建套接字
    s = socket(AF_INET, SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)

    #创建两个进程来分别独立执行
    #管理员喊话和转发客户端信息功能
    pid = os.fork()
    if pid < 0:
        sys.exit("创建进程失败") 
    elif pid == 0:
        do_child(s, ADDR)
    else:
        do_parent(s)




        


if __name__ == "__main__":
    main()