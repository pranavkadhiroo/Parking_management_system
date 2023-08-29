import mysql.connector as mys
import pickle
import datetime
import math
import matplotlib.pyplot as pyplot

f = open('config.dat','rb')   
d = pickle.load(f)
f.close()

con = mys.connect(host = 'localhost', username = d['db_username'], password = d['db_password'], database = d['db_name'])
c = con.cursor()

def check_exists(vehicle_no):
    
    c.execute("select *from vehicles where vehicle_no = '{}'".format(vehicle_no))
    c.fetchall()
    if c.rowcount == 0:
        return False
    else:
        return True

def slots():
    
    c.execute("select id, space_for, is_empty from slots")
    data = c.fetchall()
    print('Slots','\t','Space for','\t','Status')
    print()
    for i in data:
        print('Slot '+str(i[0]),'\t',i[1],'\t',i[2])
        
def add_vehicle():
    
    name = input('Enter your name\n')
    mobile = input('Enter your mobile no.\n')
    entry_time = datetime.datetime.now()
    vehicle_no = input('Enter vehicle no.\n')
    vehicle_type = input('Enter vehicle type (four seater or two seater)\n')
    q = "insert into vehicles(name, mobile, entry_time, vehicle_no, vehicle_type, created_at) values('{}','{}','{}','{}','{}','{}')".format(name, mobile, entry_time, vehicle_no, vehicle_type, entry_time)
    c.execute(q)
    con.commit()
    c.execute('select *from slots')
    data = c.fetchall()
    for i in data:
        if i[2] == vehicle_type and i[3] == 'empty':
            c.execute("update slots set vehicle_id = '{}', is_empty = 'full' where id = {}".format(vehicle_no,i[0]))
            con.commit()
            print('Vehicle Added ')
            break
    else:
        print('Parking Full!!')
    
def manage_vehicle():
    
    while True:
        
        print('1.Update vehicle details')
        print('2.Exit vehicle')
        print('3.Return to main menu')
        
        ch = int(input('Enter your choice\n'))
        if ch == 1:
            update()
        elif ch == 2:
            exit_vehicle()
        elif ch == 3:
            return
        else:
            print('Please enter a valid choice\n')
            manage_vehicle()


    
def update():
    
    vehicle_no = input('Enter the vehicle no. to be updated\n')
    if check_exists(vehicle_no) == True:
        print('1.Edit name')
        print('2.Edit mobile no.')
        ch = int(input('Enter your choice\n'))
        if ch == 1:
            name = input('Enter name\n')
            updated_at = datetime.datetime.now()
            c.execute("update vehicles set name = '{}', updated_at = '{}' where vehicle_no = '{}' ".format(name, updated_at, vehicle_no))
            con.commit()
            print('Details updated')
        elif ch == 2:
            mobile = input('Enter mobile no.\n')
            updated_at = datetime.datetime.now()
            c.execute("update vehicles set mobile = '{}', updated_at = '{}'  where vehicle_no = '{}'".format(mobile,updated_at, vehicle_no))
            con.commit()
            print('Details updated')
        else:
            print('Please enter a valid choice')
            
    else:
        print('The vehicle no. is not valid')
        manage_vehicle()
        

def exit_vehicle():
    
    vehicle_no = input('Enter the vehicle no.\n')
    if check_exists(vehicle_no) == True:
        exit_time = datetime.datetime.now()
        c.execute("update vehicles set exit_time = '{}' where vehicle_no = '{}'".format(exit_time, vehicle_no))
        con.commit()
        amt = bill(vehicle_no)
        ch = input('Pay Bill (y/n)\n')
        if ch == 'y':
            c.execute("select *from vehicles where vehicle_no = '{}'".format(vehicle_no))
            data = c.fetchall()
            data = data[0]
            q = "insert into history(name, vehicle_no, mobile, entry_time, exit_time, bill) values('{}','{}','{}','{}','{}',{})"
            c.execute(q.format(data[0], data[4], data[1], data[2], data[3], amt))
            con.commit()
            c.execute("delete from vehicles where vehicle_no ='{}'".format(vehicle_no))
            con.commit()
            c.execute("update slots set vehicle_id = NULL, is_empty = 'empty' where vehicle_id = '{}'".format(vehicle_no))
            con.commit()
            print('Thank you!!')
        elif ch == 'n':
            manage_vehicle()
        else:
            manage_vehicle()
    else:
        print('The vehicle no. is not valid')
        manage_vehicle()
        
def bill(vehicle_no):
    
    c.execute("select *from vehicles where vehicle_no = '{}'".format(vehicle_no))
    data = c.fetchall()
    data = data[0]
    amt = charge(data)
    amt = float(amt)
    print(' '*6,'BILL')
    print()
    print('Vehicle no:-','\t',data[4])
    print('Entry time:-','\t',data[2])
    print('Exit time:-','\t',data[3])
    print('Total amount:-','\t',amt,'AED')
    return float(amt)
    
def charge(data):
    
    entry_time = datetime.datetime.fromisoformat(str(data[2]))
    exit_time = datetime.datetime.fromisoformat(str(data[3]))
    time = exit_time - entry_time
    time = time.total_seconds()/3600
    if math.modf(time)[0] >=0.5:
        return (int(time)+1)*10
    else:
        return int(time)*10
def history():
    
    c.execute('select *from history')
    data = c.fetchall()
    data = data[0]
    print("%25s%25s%25s%30s%30s%20s"%('Name','Vehicle no.','Mobile no.','Entry time','Exit time','Bill'))
    print("%25s%25s%25s%30s%30s%20s"%(data[1],data[2],data[3],data[4],data[5],data[6]))
def add_admin():
    
    username = input('Enter username\n')
    password = input('Enter password\n')
    created_at = datetime.date.today()
    c.execute("insert into admin values('{}','{}','{}')".format(username,password,created_at))
    con.commit()
    print('User added')

def remove_admin():
    
    username = input('Enter admin username to be removed\n')
    c.execute('select username, password from admin')
    data = c.fetchall()
    for i in data:
        if i[0] == username:
            password = input('Enter the password\n')
            if i[1] == password:
                c.execute("delete from admin where username='{}'".format(username))
                con.commit()
                print('User deleted')
                break
            else:
                print('Incorrect password')
                break
    else:
        print('The user you have entered does not exist!')

def update_admin():
    
    username = input('Enter admin username to be updated\n')
    c.execute('select username, password from admin')
    data = c.fetchall()
    for i in data:
        if i[0] == username:
            password = input('Enter the password\n')
            if i[1] == password:
                new_user = input('Enter new username\n')
                new_pass = input('Enter new password\n')
                c.execute("update admin set username = '{}', password = '{}' where username='{}'".format(new_user,new_pass,username))
                con.commit()
                print('User updated')
                break
            else:
                print('Incorrect password')
                break
    else:
        print('The user you have entered does not exist!')

def add_slot():
    
    category = input('Enter the vehicle type(two seater, four seater)\n')
    c.execute('select id from slots')
    data = c.fetchall()
    slot_id = data[-1][0] + 1
    q = "insert into slots(id,space_for, is_empty) values({},'{}','{}')".format(slot_id,category,'empty')
    c.execute(q)
    con.commit()
    print('Slot added')

def remove_slot():
    
    slot_id = int(input('Enter the id of the slot to be removed\n'))
    c.execute("select *from slots where id = {} and is_empty = '{}'".format(slot_id,'empty'))
    data = c.fetchall()
    if data == []:
        print("Currently the slot is active, can't be removed")
    else:
        c.execute('delete from slots where id = {}'.format(slot_id))
        con.commit()
        print('Slot removed')

def report():
    
    yr = int(input('Enter the year for which report is to be displayed:\n'))
    c.execute('select exit_time, bill from history')
    data = c.fetchall()
    m = []
    for i in data:
        if i[0].year == yr:
            m.append(i)
    d = {'Jan':0,'Feb':0,'Mar':0,'Apr':0,'May':0,'Jun':0,'Jul':0,'Aug':0,'Sep':0,'Oct':0,'Nov':0,'Dec':0}
    for j in m:
        if j[0].month == 1:
            d['Jan'] += float(j[1])
        elif j[0].month == 2:
            d['Feb'] += float(j[1])
        elif j[0].month == 3:
            d['Mar'] += float(j[1])
        elif j[0].month == 4:
            d['Apr'] += float(j[1])
        elif j[0].month == 5:
            d['May'] += float(j[1])
        elif j[0].month == 6:
            d['Jun'] += float(j[1])
        elif j[0].month == 7:
            d['Jul'] += float(j[1])
        elif j[0].month == 8:
            d['Aug'] += float(j[1])
        elif j[0].month == 9:
            d['Sep'] += float(j[1])
        elif j[0].month == 10:
            d['Oct'] += float(j[1])
        elif j[0].month == 11:
            d['Nov'] += float(j[1])
        elif j[0].month == 12:
            d['Dec'] += float(j[1])
    months = []
    bill = []
    for x,y in d.items():
        months.append(x)
        bill.append(y)
    pyplot.bar(months,bill)
    pyplot.show()        



        
            
    



    
    
    
    
    
        
    
    