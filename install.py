import pickle

print('Installtion - Parking Mangement System')

db_name = input('Enter database name\n')
db_username = input('Enter database username\n')
db_password = input('Enter database password\n')
two_seater = int(input('Enter the space for two seater\n'))
four_seater = int(input('Enter the space for four seater\n'))
admin_username = input('Enter admin username\n')
admin_password = input('Enter admin password\n')
d = {'db_name':db_name,'db_username':db_username,'db_password':db_password,'two_seater':two_seater,'four_seater':four_seater,'admin_username':admin_username,'admin_password':admin_password}

f = open('config.dat','wb')
pickle.dump(d,f)
f.close()

import create_tables 
import run




  

        
