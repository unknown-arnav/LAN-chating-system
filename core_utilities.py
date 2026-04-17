import mysql.connector as m 
db=m.connect(host='localhost' ,user='root' ,password='system')
cur=db.cursor()
cur.execute("use chatroom")
usna='arnav'
cur.execute(f"select * from users where usna='{usna}' limit 1")
p=cur.fetchone() is not None
print(p)