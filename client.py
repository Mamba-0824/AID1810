from socket import *
import sys, os

#发送消息
def send_msg(s, name, addr):
    while True:
        text = input("发言:")
        if text.strip() == 'quit':
            msg = 'Q ' + name
            s.sendto(msg.encode(), addr)
            sys.exit("退出聊天室")

        msg = 'C %s %s' % (name, text)
        s.sendto(msg.encode(), addr)

#接受消息
def recv_msg(s):
    while True:
        data, addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)

        print(data.decode(), '\n发言:', end='')

# 创建套接字，登录，创建子进程
def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)

    #创建套接字
    s = socket(AF_INET, SOCK_DGRAM)
    #以下是客户端登录进入聊天室程序
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        s.sendto(msg.encode(), ADDR)
        #等待服务器回复
        data, addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室")
            break 
        else:
            #不成功服务端会回复不允许登录原因
            print(data.decode())
    
    #创建父子进程,分别用来接受服务器数据，
    #同时又可以发表会话信息
    pid = os.fork()
    if pid < 0:
        sys.exit("创建子进程失败")
    elif pid == 0:
        send_msg(s, name, ADDR)
    else:
        recv_msg(s)




if __name__ == "__main__":
    main()

