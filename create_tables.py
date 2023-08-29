import mysql.connector as mys
import pickle
import datetime

f = open('config.dat','rb')   
d = pickle.load(f)
f.close()
    
con = mys.connect(host = 'localhost', username = d['db_username'], password = d['db_password'])
c = con.cursor()
    
def create_tables(db_username, db_password, db_name):
    
    c.execute("create database {}".format(db_name))
    c.execute("use {}".format(db_name))
    c.execute("create table admin(username varchar(30), password varchar(30), created_at date )")
    c.execute("create table slots(id int(255) primary key, vehicle_id varchar(30), space_for varchar(30), is_empty varchar(30) default 'empty')")
    c.execute("create table vehicles(name varchar(30), mobile varchar(30),entry_time datetime, exit_time datetime, vehicle_no varchar(30), vehicle_type varchar(30), created_at datetime, updated_at datetime )")
    c.execute("create table history(id int(255) auto_increment primary key, name varchar(30), vehicle_no varchar(30), mobile varchar(30), entry_time datetime, exit_time datetime, bill float )")

def insert_slot():
    
    q = "insert into slots(id,space_for) values({},'{}')"
    slot_id = 1
    for i in range(d['two_seater']):
        c.execute(q.format(slot_id,'two seater'))
        con.commit()
        slot_id +=1
    for j in range(d['four_seater']):
        c.execute(q.format(slot_id,'four seater'))
        con.commit()
        slot_id+=1

def insert_admin():
    
    c.execute("insert into admin(username, password, created_at) values('{}','{}','{}')".format(d['admin_username'], d['admin_password'],datetime.date.today()))
    con.commit()
    
create_tables(d['db_username'],d['db_password'], d['db_name'])
insert_slot()
insert_admin() 
c.close()  
con.close() 
    
    