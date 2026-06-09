import socket
import threading
host='10.97.139.167'
port_1=55555
port_2=55556
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port_2))
server.listen()
print("Kernel started")
acti=set()

erro={'e1':'Invalid operator selected. Please try again.'}

def homepage(c,cl,usna):
    c.send(f'!!P!!-----------welcome-{usna}----------\n==============================================================================\nyou can perform various operation like:\n1--Message a friend\n2--make an user your friend\n3--friends requests\n4--check and modify your profile\n5--logout\n==============================================================================\nYou can perform any of the above operation by:\n i--typing keywords anytime(to display the keywords enter ///keywords any time)\nii--launching a popup menu and selecting any operation(to launch popup menu type ///menu)\n=============================================================================='.encode())
    c.send("ienter any operation(1-5)::".encode())
    m=c.recv(1024).decode()
    c.send("!!P!!Working on this shit".encode())

def signin(c,cl):
    while True:
        c.send('iEnter user Name::'.encode())
        un=c.recv(1024).decode()
        cl.send(f'ch-exis{un}'.encode())
        m=cl.recv(1024).decode()
        if m=='no':
            break
        else:
            c.send('!!P!!Username already exists\nPlease try again.\n'.encode())
    c.send('iEnter Password::'.encode())
    pas=c.recv(1024).decode()
    c.send('iEnter security word::'.encode())
    sec=c.recv(1024).decode()
    cl.send(f"regis{un}!@#{pas}!@#{sec}".encode())
    m=cl.recv(1024).decode()
    if m=='1':
        usna=un
        # acti.add(usna)
        homepage(c,cl,usna)
        # acti.remove(un)

def login(c,cl):
    while True:
        c.send('iEnter user Name::'.encode())
        un=c.recv(1024).decode()
        cl.send(f'ch-exis{un}'.encode())
        m=cl.recv(1024).decode()
        if m=='no':
            c.send("!!P!!Username doesn't exists\nPlease try again.".encode())
        else:
            break
    while True:
        c.send('iEnter Password::'.encode())
        pa=c.recv(1024).decode()
        if pa=='!@#':
            c.send('iEnter Security key::'.encode())
            se=c.recv(1024).decode()
            cl.send(f"ch-sec{un}::{se}".encode())
            m=cl.recv(1024).decode()
            if m=='yes':
                # acti.add(un)
                homepage(c,cl,un)
                # acti.remove(un)
                break
            else:
                c.send('!!P!!Incorrect Key entered\nTry entering password again\nEnter !@# if you forgot your password'.encode())
        else:
            cl.send(f"ch-pas{un}::{pa}".encode())
            m=cl.recv(1024).decode()
            if m=='yes':
                # acti.add(un)
                homepage(c,cl,un)
                # acti.remove(un)
                break
            else:
                c.send('!!P!!Password incorrect\nTry Again\nEnter !@# if you forgot your password'.encode())

def login_page(c,cl):
    while True:
        l="!!P!!==============================================================================\n----------------------------------------WELCOME-------------------------------\nplease select one of the following operations\n==============================================================================\n1: To create a new account\n2:To login into an existing account"
        c.send(l.encode('ascii'))
        while True:
            c.send('i::'.encode('ascii'))
            o=c.recv(1024).decode('ascii')
            if o=='1':
                signin(c,cl)
                break
            elif o=='2':
                login(c,cl)
                break
            else:
                c.send(('!!P!!'+erro['e1']).encode())

def handle(c):
    try:
        cl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cl.connect((host,port_1))
        print("Connected to core")
        while True:
            m=c.recv(1024).decode('ascii')
            if m=='hello':
                login_page(c,cl)
                continue
    except:
        print("Something went wrong")
        print(f"Closing connection{c}")
        c.close()

def req():
    while True:
        c,a=server.accept()
        print(f'Connected with address {a}')
        print(f'Connected with address {c}')

        th=threading.Thread(target=handle,args=(c,))
        th.start()

if __name__=='__main__':req()