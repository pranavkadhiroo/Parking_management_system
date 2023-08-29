import pickle
print("PARKING MANAGEMENT SYSTEM")
print()
print(' '*6+"LOGIN")

def check():
    
    import mysql.connector as mys
    username = input('Enter admin username\n')
    password = input('Enter admin password\n')
    f = open('config.dat','rb')   
    d = pickle.load(f)
    f.close()
    con = mys.connect(host = 'localhost', username = d['db_username'], password = d['db_password'], database = d['db_name'])
    c = con.cursor()
    c.execute("select username, password from admin where username = '{}'".format(username))
    data = c.fetchall()
    if len(data) == 0:
        print('The username or password you have entered is incorrect')
        return check()
    elif username == str(data[0][0]) and password == str(data[0][1]):
        c.close()
        con.close()
        return True
    else:
        print('The username or password you have entered is incorrect')
        return check()
