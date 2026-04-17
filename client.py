import socket
import time

def tame(x):
    time.sleep(x)


host='10.203.66.167'
port=55556
cl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cl.connect((host,port))
cl.send("hello".encode('ascii'))
print("!!!Connected to the server!!!")

def pint(m):
    print(m)
def inu(s):
    m=input(s)
    cl.send(m.encode('ascii'))

while True:
    a=cl.recv(1024).decode('ascii')
    if not a:
        cl.close()
        cl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cl.connect((host,port))
        cl.send("hello".encode('ascii'))
    elif a.startswith("!!P!!"):
        pint(a[5:])
    elif a[0]=='i':
        inu(a[1:])
    else:
        print('error from kernel')
        cl.close()