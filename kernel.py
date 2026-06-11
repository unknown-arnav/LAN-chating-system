import socket
import threading
import time
host='192.168.173.229'
port_1=55555
port_2=55556
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port_2))
server.listen()
print("Kernel starting")
time.sleep(3)
print("Kernel started")
acti=dict()
para=True
logs=[]
ac_conn=set()

erro={'e1':'Invalid operator selected. Please try again.'}

#Utilities(User Seaching)
def searc(cl,un):
    cl.send(f"f-un{un}")
    m=cl.recv(2056).decode()
    return m.split("::") if m!="NF" else []



#Functionalities
def frndreq():pass
def msgsnd():pass
def msglod():pass

def homepage(c,cl,usna,a):
    while True:
        global acti
        acti[a]=usna
        c.send(f'!!P!!-----------welcome-{usna}----------\n==============================================================================\nyou can perform various operation like:\n1--Message a friend\n2--make an user your friend\n3--friends requests\n4--check and modify your profile\n5--logout\n==============================================================================\nYou can perform any of the above operation by:\n i--typing keywords anytime(to display the keywords enter ///keywords any time)\nii--launching a popup menu and selecting any operation(to launch popup menu type ///menu)\n=============================================================================='.encode())
        c.send("ienter any operation(1-5)::".encode())
        m=c.recv(1024).decode()
        if m=='5':
            c.send("!!P!!Logging out and returning to login page".encode())
            acti.pop(a,None)
            break
        else:c.send("!!P!!Working on this shit".encode())

# handling the logins
def signin(c,cl,a):
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
        homepage(c,cl,un,a)

def login(c,cl,a):
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
                homepage(c,cl,un,a)
                break
            else:
                c.send('!!P!!Incorrect Key entered\nTry entering password again\nEnter !@# if you forgot your password'.encode())
        else:
            cl.send(f"ch-pas{un}::{pa}".encode())
            m=cl.recv(1024).decode()
            if m=='yes':
                homepage(c,cl,un,a)
                break
            else:
                c.send('!!P!!Password incorrect\nTry Again\nEnter !@# if you forgot your password'.encode())

def login_page(c,cl,a):
    while True:
        l="!!P!!==============================================================================\n----------------------------------------WELCOME-------------------------------\nplease select one of the following operations\n==============================================================================\n1: To create a new account\n2:To login into an existing account"
        c.send(l.encode('ascii'))
        while True: 
            time.sleep(0.1)
            c.send('i::'.encode('ascii'))
            o=c.recv(1024).decode('ascii')
            if o=='1':signin(c,cl,a);break
            elif o=='2':login(c,cl,a);break
            else:c.send(('!!P!!'+erro['e1']).encode())




# handling the connections
def handle(c,a):
    global ac_conn,acti
    try:
        cl=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cl.connect((host,port_1))
        ac_conn.add(a)
        while True:
            m=c.recv(1024).decode('ascii')
            if m=='hello':
                login_page(c,cl,a)
                continue
    except:
        global para,logs
        if para:print(f"Closing connection{c}")
        else:logs.append((1,c))
        c.close()
        ac_conn.discard(a)
        acti.pop(a,None)

def req():
    while True:
        c,a=server.accept()
        if para:print();print(f'Connected with address {a}')
        else:logs.append((0,a))
        th=threading.Thread(target=handle,args=(c,a,))
        th.start()



# handling the admin controls
def control():
    global para
    para=False
    global logs
    print("Optimised State active now")
    print("To switch to logs enter::alpha")
    print("To print the active connections, enter::gamma")
    print("To print the active connections, enter::delta")
    while True:
        try:
            o=input("Select operation::")
            if o=="alpha":
                if not logs:print("No activity detected since Optimised state was actived")
                for s,a in logs:print(f'Connected with address {a}' if s==0 else f"Closing connection{a}")
                para=True
                logs=[]
                print("To go back to optimised state select any operation or enter beta")
            elif o=="beta":
                para=False
                print("Returning to optimised state")
            elif o=="gamma":
                print("Number of active conn on this kernel::",len(ac_conn))
                for i in ac_conn:print(i)
                para=False
                print("Returning to optimised state")
            elif o=="delta":
                print("Number of logged in users on this kernel::",len(acti))
                for x,y in acti.items():print(x,y)
                para=False
                print("Returning to optimised state")
            else:print("Invalid operation used")
        except Exception as e:print(f"internal error occured due to admin's input. Error details{e}")



# initiating everything
t_main=threading.Thread(target=control,args=())
t_main.start()
if __name__=='__main__':req()