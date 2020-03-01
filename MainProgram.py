import sqlite3
from sqlite3 import Error


def login():
    uname = 'admin123'
    pword = '123456'

    for i in range(0,3):
        input1 = input("Enter Username: ")
        input2 = input("Enter Password: ")
        if (input1 == uname) & (input2 == pword):
            selectOptions()
            break;
        else:
            if (i == 0) | (i == 1):
                print("Please Try again..")
            else:
                print("Sorry please contact your admin.")

def selectOptions():

    exit = False;

    while(exit == False):
        print("Please select option: ")
        print("1. Create new account")
        print("2. Update account")
        print("3. Delete account")
        print("4. View account")
        print("5. View accounts")
        print("6. Deposit account")
        print("7. Withdraw money")
        print("8. Exit")
        select1 = input("Enter your choice number: ")

        if (select1 == "1"):
            createNewAcc()
        elif (select1 == "2"):
            updateAcc()
        elif (select1 == "3"):
            delAcc()
        elif (select1 == "4"):
            viewAcc()
        elif (select1 == "5"):
            viewAccs()
        elif (select1 == "6"):
            depositAcc()
        elif (select1 == "7"):
            withdrawAcc()
        else:
            exit=True;
            print("Thankyou for using our system.")



def createNewAcc():
    customer = ["Default","Default","Default","Default","Default","Default","Default"]
    customer[0] = input("Enter your First Name: ")
    customer[1] = input("Enter your Last Name: ")
    customer[2] = input("Enter your Address: ")
    customer[3] = input("Enter your City: ")
    customer[4] = input("Enter Phone number: ")
    customer[5] = input("Your Account Balance: ")
    customer[6] = input("Enter PIN: ")

    createDB()
    insertCustomer(customer)

def updateAcc():
    uid = int(input("Please enter your ID: "))
    exist = checkCustomer(uid)
    if (exist == True):
        correct = checkPIN(uid)
        if (correct == True):
            print("What do you want to update?")
            print("1. Your Address")
            print("2. Your City")
            print("3. Your Phone Number")
            print("4. Your PIN")
            select2 = input("Enter your choice number: ")

            if (select2 == "1"):
                col = "Address"

            elif (select2 == "2"):
                col = "City"

            elif (select2 == "3"):
                col = "PhoneNumber"

            elif (select2 == "4"):
                col = "PIN"
            else:
                return

            temptext = "Enter " + col + ": "
            value = input(temptext)

            updateCustomer(col, value, uid)
            print("Your account updated successfully.")
        else:
            return

    else:
        print("ID not found")
        return

def delAcc():
    uid1 = int(input("Please enter your ID: "))
    exist = checkCustomer(uid1)
    if (exist == True) :
        correct = checkPIN(uid1)
        if (correct == True):
            delCustomer(uid1)
            print("Your account deleted successfully.")
        else:
            return
    else:
        print("ID not found")
        return


def viewAcc():
    uid4 = int(input("Please enter your ID: "))
    exist = checkCustomer(uid4)
    if (exist == True):
        correct = checkPIN(uid4)
        if (correct == True):
            con = sqlite3.connect('BankCustomerPortal.db')
            cursorObj = con.cursor()
            cursorObj.execute("SELECT * FROM Customer_Info where ID = " + str(uid4))
            acc = cursorObj.fetchone()
            print("First Name\tLast Name\tAddress\tCity\tPhoneNumber\tAccountBalance")
            print(acc[1] + "\t" + acc[2] + "\t" + acc[3] + "\t" + acc[4] + "\t" + str(acc[5]) + "\t" + str(acc[6]))
        else:
            return

    else:
        print("ID not found")
        return

def viewAccs():
    con = sqlite3.connect('BankCustomerPortal.db')
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM Customer_Info")
    accs = cursorObj.fetchall()
    for acc in accs:
        print("First Name\tLast Name\tAddress\tCity\tPhoneNumber\tAccountBalance")
        print(acc[1] + "\t" + acc[2] + "\t" + acc[3] + "\t" + acc[4] + "\t" + str(acc[5]) + "\t" + str(acc[6]))

def withdrawAcc():
    uid3 = int(input("Please enter your ID: "))
    exist = checkCustomer(uid3)
    if (exist == True):
        correct = checkPIN(uid3)
        if (correct == True):
            subtracting = int(input("How much money do you want to withdraw? "))
            withdrawAmount(uid3, subtracting)
            print("You successfully withdraw your amount Thank you.")
        else:
            return

    else:
        print("ID not found")
        return

def depositAcc():
    uid2 = int(input("Please enter your ID: "))
    exist = checkCustomer(uid2)
    if (exist == True):
        correct = checkPIN(uid2)
        if (correct == True):
            adding = int(input("How much money do you want to deposit? "))
            depositAmount(uid2, adding)
            print("Your amount successfully deposited Thank you.")
        else:
            return

    else:
        print("ID not found")
        return


def createDB():
    con = sqlite3.connect("BankCustomerPortal.db")
    cursorObj = con.cursor()
    cursorObj.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Customer_Info' ''')

    if (cursorObj.fetchone()[0] == 1):
        print("Table already exist.")
    else:
        try:
            con = sqlite3.connect('BankCustomerPortal.db')
            cursorObj.execute(
                "CREATE TABLE Customer_Info(ID integer PRIMARY KEY AUTOINCREMENT, FirstName text, LastName text, Address text, City text, PhoneNumber text, AccountBalance text, PIN text)")
            con.commit()
        except Error:
            print(Error)


def insertCustomer(customer):
    con = sqlite3.connect('BankCustomerPortal.db')
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO Customer_Info (FirstName, LastName, Address, City, PhoneNumber, AccountBalance, PIN) VALUES(?, ?, ?, ?, ?, ?, ?)", customer)
    cursorObj.execute('SELECT ID FROM Customer_Info WHERE id=(SELECT max(id) FROM Customer_Info)')
    cid = cursorObj.fetchone()[0]
    print("Your ID is ", cid, " . Remember your ID next time.")
    con.commit()

def updateCustomer(columnName, Value, uid):
    con = sqlite3.connect('BankCustomerPortal.db')
    query = "UPDATE Customer_Info SET " + columnName + "=\"" + Value + "\" where id = " + str(uid)
    cursorObj = con.cursor()
    cursorObj.execute(query)
    con.commit()

def delCustomer(uid1):
    con = sqlite3.connect('BankCustomerPortal.db')
    query1 = "DELETE FROM Customer_Info where id = " + str(uid1)
    cursorObj = con.cursor()
    cursorObj.execute(query1)
    con.commit()

def checkCustomer(id):
    con = sqlite3.connect('BankCustomerPortal.db')
    query2 = "SELECT count(ID) FROM Customer_Info where ID = " + str(id)
    cursorObj = con.cursor()
    cursorObj.execute(query2)
    if (cursorObj.fetchone()[0] == 1):
        return True
    else:
        return False
def depositAmount(uid2, adding):
    con = sqlite3.connect('BankCustomerPortal.db')
    cursorObj = con.cursor()
    cursorObj.execute("SELECT AccountBalance FROM Customer_Info where id = " + str(uid2))
    accBalance = cursorObj.fetchone()[0]
    accBalance = int(accBalance) + adding
    query3 = "UPDATE Customer_Info SET AccountBalance=\""+ str(accBalance) +"\" where id = " + str(uid2)
    cursorObj.execute(query3)
    con.commit()

def withdrawAmount(uid3, subtracting):
    con = sqlite3.connect('BankCustomerPortal.db')
    cursorObj = con.cursor()
    cursorObj.execute("SELECT AccountBalance FROM Customer_Info where id = " + str(uid3))
    accBalance = cursorObj.fetchone()[0]
    accBalance = int(accBalance) - subtracting
    query4 = "UPDATE Customer_Info SET AccountBalance=\"" + str(accBalance) + "\" where id = " + str(uid3)
    cursorObj.execute(query4)
    con.commit()

def checkPIN(uID):
    for i in range(0, 3):
        pWord = input("Please enter your PIN code: ")
        con = sqlite3.connect('BankCustomerPortal.db')
        cursorObj = con.cursor()
        cursorObj.execute("SELECT PIN FROM Customer_Info where id = " + str(uID))
        check = cursorObj.fetchone()[0]
        if (pWord == check):
            return True
        else:
            print("Incorrect PIN.")
    return False

login()



