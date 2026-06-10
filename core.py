print("Starting the Core")
import time
import threading 
import socket
import mysql.connector as mm
host='10.97.139.167'
port=55555
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#Utility VAriables
sdb=mm.connect(host="localhost",user="root",password="system")
scur=sdb.cursor()
reg=set()


def func(c):
    db=mm.connect(host='localhost',user='root',password='system')
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
            if p[0]==l[1]:c.send("yes".encode())
            else:c.send("no".encode())
        elif m.startswith("ch-sec"):
            m=m[6:]
            l=m.split("::")
            cur.execute(f"select sec from users where usna='{l[0]}' limit 1")
            p=cur.fetchone()
            if p[0]==l[1]:c.send("yes".encode())
            else:c.send("no".encode())
        elif m.startswith("f-un"):
            un=m[4:]
            l=[]
            for i in reg:
                if un in i:l.append(i)
            if l:c.send('::'.join(l).encode())
            else:c.send("NF".encode())
        else:
            db.close()
            print('Unidentified operation used somewhere')
            print(m)
            c.close()
            break

def req():
    print("Core started")
    while True:
        try:
            c,a=server.accept()
            print(f'Connected with address {a}')
            th=threading.Thread(target=func,args=(c,))
            th.start()
        except:print("Error")

#MainTaining functions 
def maint():
    global reg
    while True:
        scur.execute("use chatroom")
        scur.execute("select usna from users")
        t=set()
        while True:
            a=scur.fetchone()
            if a is None:break
            t.add(a[0])
        reg=t.copy()
        time.sleep(60)
        


t=threading.Thread(target=maint,args=())
t.start()
time.sleep(1)
if __name__=="__main__":req()