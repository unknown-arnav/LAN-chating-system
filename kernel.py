import socket
import threading
import time
host='192.168.175.227'
port_1=55555
port_2=55556
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port_2))
server.listen()
print("Kernel starting")
time.sleep(3)
print("Kernel started")
acti=set()

erro={'e1':'Invalid operator selected. Please try again.'}



# handling the logins
def homepage(c,cl,usna):
    while True:
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
        acti.add(un)
        homepage(c,cl,un)
        acti.remove(un)

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
                acti.add(un)
                homepage(c,cl,un)
                acti.remove(un)
                break
            else:
                c.send('!!P!!Incorrect Key entered\nTry entering password again\nEnter !@# if you forgot your password'.encode())
        else:
            cl.send(f"ch-pas{un}::{pa}".encode())
            m=cl.recv(1024).decode()
            if m=='yes':
                acti.add(un)
                homepage(c,cl,un)
                acti.remove(un)
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
            elif o=='2':
                login(c,cl)
            else:
                c.send(('!!P!!'+erro['e1']).encode())




# handling the connections
def handle(c):
    try:
        cl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cl.connect((host,port_1))
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
        if para:print(f'Connected with address {a}')
        else:logs.append(a)
        th=threading.Thread(target=handle,args=(c,))
        th.start()



# handling the admin controls
para=True
logs=[]
def control():
    global para
    para=False
    global logs
    print("Optimised State active now")
    print("To switch to logs enter::alpha")
    print("To print the active users, enter::gamma")
    while True:
        try:
            o=input("Select operation::")
            if o=="alpha":
                if not logs:print("No activity detected since Optimised state was actived")
                for a in logs:print(f'Connected with address {a}')
                para=True
                logs=[]
                print("To go back to optimised state select any operation or enter beta")
            elif o=="beta":
                para=False
                print("Returning to optimised state")
            elif o=="gamma":
                print("Number of active users on this kernel::",len(acti))
                for i in acti:print(i)
                para=False
                print("Returning to optimised state")
            else:print("Invalid operation used")

        except Exception as e:
            print(f"internal error occured due to user's input. Error details{e}")



# initiating everything
t_main=threading.Thread(target=control,args=())
t_main.start()
if __name__=='__main__':req()