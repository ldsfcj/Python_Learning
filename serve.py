import socket
import threading
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#然后，我们要绑定监听的地址和端口。服务器可能有多块网卡，可以绑定到
#某一块网卡的IP地址上，也可以用0.0.0.0绑定到所有的网络地址，还可以
#用127.0.0.1绑定到本机地址。127.0.0.1是一个特殊的IP地址，表示本机
#地址，如果绑定到这个地址，客户端必须同时在本机运行才能连接，也就是说
#，外部的计算机无法连接进来。

#端口号需要预先指定。因为我们写的这个服务不是标准服务，所以用9999这个
#端口号。请注意，小于1024的端口号必须要有管理员权限才能绑定：
s.bind(('127.0.0.1', 9999))#监听端口

#紧接着，调用listen()方法开始监听端口，传入的参数指定等待连接的最大数量
s.listen(5)
print('Waiting for connection...')

#接下来，服务器程序通过一个永久循环来接受来自客户端的连接，accept()会
#等待并返回一个客户端的连接
def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(3)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

while True:
    #接受一个新连接：
    sock, addr = s.accept()
    #创建新线程来处理TCP连接
    t = threading.Thread(target=tcplink, args=(sock,addr))
    t.start()
    