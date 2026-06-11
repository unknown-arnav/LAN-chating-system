print("Starting the Core")
import time
import threading 
import socket
import mysql.connector as mm
host='192.168.173.229'
port=55555
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

#Utility VAriables
sdb=mm.connect(host="localhost",user="root",password="system")
scur=sdb.cursor()
reg=set()
def regi(cur,un):
    cur.execute(f"create database {un}")
    cur.execute(f"use {un}")
    cur.execute("create table if not exists msg (send_to varchar(50),msg varchar(500),date date,time time)")
    cur.execute("create table if not exists frnd (usna varchar(50))")
    cur.execute("create table if not exists frndreq (req varchar(50),waiting_frmd date)")
    cur.execute("create table if not exists unrd (fro varchar(50))")


def func(c):
    db=mm.connect(host='localhost',user='root',password='system')
    cur=db.cursor()
    while True:
        cur.execute("use chatroom")
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
            regi(cur,l[0])
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
        #not finished not tested
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