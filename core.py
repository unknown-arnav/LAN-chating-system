import threading 
import socket
host='10.203.66.167'
port=55555
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
print("Core started")


def func(c):
    import mysql.connector as m
    db=m.connect(host='localhost',user='root',password='system')
    cur=db.cursor()
    cur.execute("use chatroom")
    while True:
        m=c.recv(1024).decode()
        if m.startswith("ch-exis"):
            u=m[7:]        
            cur.execute(f"select * from users where usna='{u}' limit 1")
            p=cur.fetchone() is not None
            if p:me="yes".encode()
            else:me='no'.encode()
            c.send(me)
        elif m.startswith("regis"):
            l=m[5:].split('!@#')
            cur.execute(f"insert into users(usna,pas,sec) values('{l[0]}','{l[1]}','{l[2]}')")
            cur.execute("commit")
            c.send("1".encode())
        elif m.startswith("ch-pas"):
            m=m[6:]
            l=m.split("::")
            cur.execute(f"select pas from users where usna='{l[0]}' limit 1")
            p=cur.fetchone()
            if p[0]==l[1]:
                c.send("yes".encode())
            else:
                c.send("no".encode())
        elif m.startswith("ch-sec"):
            m=m[6:]
            l=m.split("::")
            cur.execute(f"select sec from users where usna='{l[0]}' limit 1")
            p=cur.fetchone()
            if p[0]==l[1]:
                c.send("yes".encode())
            else:
                c.send("no".encode())
        else:
            print('Unidentified operation used somewhere')
def req():
    while True:
        try:
            c,a=server.accept()
            print(f'Connected with address {a}')
            th=threading.Thread(target=func,args=(c,))
            th.daemon=True
            th.start()
        except:
            print("Error")
        
req()