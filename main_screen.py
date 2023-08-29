import main_op as op

print(' '*25,'Welcome to Parking Mangement System')
print()

while True:
        
    print('1.Display Parking Slots')
    print('2.Add vehicle')
    print('3.Manage vehicle')
    print('4.History')
    print('5.Admin settings')
    print('6.Manage Parking slots')
    print('7.Show monthy report')
    print('8.Exit')
    
    ch = int(input('Enter your choice\n'))
    if ch == 1:
        op.slots()
    elif ch==2:
        op.add_vehicle()
    elif ch==3:
        op.manage_vehicle()
    elif ch==4:
        op.history()
    elif ch==5:
        while True:
            print('1.Add admin')
            print('2.Remove admin')
            print('3.Update admin')
            print('4.Return to main menu')
            cho = int(input('Enter your choice\n'))
            if cho == 1:
                op.add_admin()
            elif cho == 2:
                op.remove_admin()
            elif cho == 3:
                op.update_admin()
            elif cho == 4:
                break
            else:
                print('Please enter valid choice')
    elif ch == 6:
        while True:
            print('1.Add slot')
            print('2.Remove admin')
            print('3.Return to main menu')
            ch1 = int(input('Enter your choice\n'))
            if ch1 == 1:
                op.add_slot()
            elif ch1 == 2:
                op.remove_slot()
            elif ch1 == 3:
                break
            else:
                print('Please enter valid choice')
    elif ch == 7:
        op.report()
    elif ch == 8:
        print('Thank You!')
        break
    else:
        print('Please enter a valid choice')        