# implementing double ended queue system
import json
import time
import threading
socket=""
def rec():
    m=socket.recv(1024).decode("ascii")
    d=json.loads(m)
    return d
def sen(d):
    l=json.dumps(d)
    socket.sendall(l.encode("UTF-8"))
    return "Dn"
L=[]
def bt():
    while True:
        time.sleep(5)
        data = {"name": "Alice", "age": 30, "city": "New York"}
        for _ in range(10):L.append(json.dumps(data))
        print(L)
def bt1():
    while True:
        time.sleep(3)
        while len(L)!=0:
            L.pop()
        print(L)

th=threading.Thread(target=bt,args=())
th.start()
t=threading.Thread(target=bt1,args=())
t.start()