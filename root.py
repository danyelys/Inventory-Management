import re
import time

from tkinter import * 
from tkinter import messagebox
from tkinter import ttk
from dateutil.relativedelta import relativedelta
from datetime import datetime,date
import tkinter.font as font
from mongodb_accessors import *
from sqlpackage import establish_connection, read_query, execute_query, tables_init, reconnect, re_init


#Insert SQL Password under YourSQLPW
connection = establish_connection("localhost", "root", "2odeTOviceroy2")
connection = tables_init(connection)


## admin registration password ##
adminpassword = 123456

## testing for warranty functionality ##
today = date.today()
d1 = today.strftime('%Y-%m-%d' )
test_warranty = '2023-1-1'

date_input = d1


## global tkinter sizes ##
global pageGeometry
global pageHeight
global pageWidth
global buttonHeight
global buttonWidth

pageGeometry = '1280x720'
pageHeight = 1280
pageWidth = 720
buttonHeight = 50
buttonWidth = 150
button_font = 'Verdana 9 bold'

## global search input variables ##
global categoryInput
global modelInput
global priceInput
global colourInput
global factoryInput
global productionYearInput
global idSearchInput

## pop-out window boolean indicators ##
purchaseWindow = False
requestWindow = False
adminWindow = False



## Other Functions ##
regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  

def ifSpace(string):
    for i in string:
        if i == " ":
            return True
    return False
        

## loginPage ##
def loginToMainPage():
    loginPage.destroy()
    mainPageFunction()

def loginToRegPage():
    loginPage.destroy()
    regPageFunction()
    
def loginToAdminRegPage():
    loginPage.destroy()
    AdminregPageFunction()
    global adminWindow
    adminWindow = False
    
def logintoAdminPassword():
    AdminPasswordFunction()

def destroyAdminPassword():
    global adminWindow
    adminWindow = False
    Passwordpage.destroy()

def AdminPasswordFunction():
    password1=str(adminpassword)
    global Passwordpage
    global adminWindow
    if not adminWindow:
        Passwordpage = Toplevel()
        Passwordpage.title('Admin Password')
        Passwordpage.geometry('260x180')
        my_label = Label(Passwordpage, image=rainbow, font=button_font)
        my_label.place(x=0,y=0,relwidth=1,relheight=1)
        Label(Passwordpage, text = 'Enter Authentication Password:', font=button_font).place(x = 20, y = 10, height = 20, width = 220)
        password = StringVar()
        passwordEntry = Entry(Passwordpage, textvariable = password, font=button_font)
        passwordEntry.place(x = 60, y = 50, height = buttonHeight, width = buttonWidth)
        adminWindow = True
    else:
        return messagebox.showerror(title = 'Error', message = 'Multiple Admin Passoword windows opened')
    def verifypassword():
        pinput=passwordEntry.get()
        global adminWindow
        adminWindow = False
        if pinput==password1:
            Passwordpage.destroy()
            loginToAdminRegPage()
        else:
            passwordEntry.delete(0, END)
            Passwordpage.destroy()
            return messagebox.showerror(title = 'Wrong Admin Password', message = 'Incorrect password')
    enterButton = Button(Passwordpage, text = 'Enter', command = verifypassword, font=button_font)
    enterButton.place(x = 130 - buttonWidth/4*3, y =110 , height = buttonHeight, width = buttonWidth/2)
    cancelButton = Button(Passwordpage, text = 'Cancel', command = destroyAdminPassword, font=button_font)
    cancelButton.place(x = 130 + buttonWidth/4, y =110 , height = buttonHeight, width = buttonWidth/2)
            

    
def loginPageFunction():
    global loginPage
    loginPage = Toplevel()
    loginPage.title('Login Page')
    loginPage.geometry(pageGeometry)
    my_label = Label(loginPage, image=pink)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    Label(loginPage,image=oshes2).place(x = (pageHeight/2 - 210), y = 0, height = 100, width = 360)

    



    Label(loginPage, text = 'User ID',font=button_font).place(x = (pageHeight/2 - 200), y = 150, height = buttonHeight, width = buttonWidth)
    userID = StringVar()
    userIDEntry = Entry(loginPage, textvariable = userID)
    userIDEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 150, height = buttonHeight, width = buttonWidth)

    Label(loginPage, text = 'Password',font=button_font).place(x = (pageHeight/2 - 200), y = 250, height = buttonHeight, width = buttonWidth)
    password = StringVar()
    passwordEntry = Entry(loginPage, textvariable = password, show = '*')
    passwordEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 250, height = buttonHeight, width = buttonWidth)
    
    def verifyLogin():

        userIDInput = userIDEntry.get()
        passwordInput = passwordEntry.get()
        verifyquery="SELECT * FROM customers WHERE CustomerID = '%s' AND password = '%s' "%(userIDInput,passwordInput)
        verifyquery2="SELECT * FROM admins WHERE AdminID = '%s' AND password = '%s' "%(userIDInput,passwordInput)

        userIDEntry.delete(0, END)
        passwordEntry.delete(0, END)

        #use userIDInput and passwordInput to check login, run query to verify

        reading=read_query(connection,verifyquery)
        reading2=read_query(connection,verifyquery2)
        global CurrentUserID
        CurrentUserID=None

        global userStatus
        userStatus = ''
        if len(reading)>=1:
            userStatus='Customer'
            CurrentUserID=userIDInput
            loginToMainPage()
            return messagebox.showinfo(title = 'Login Successful', message = 'Welcome Customer,You have successfully Login!')
        if len(reading2)>=1:
            userStatus='Admin'
            CurrentUserID=userIDInput
            loginToMainPage()
            return messagebox.showinfo(title = 'Login Successful', message = 'Welcome Admin, You have successfully Login!')
        else:
            return messagebox.showerror(title = 'Registration Unsuccessful', message = 'Incorrect Username or Password, Please try again')
        
    loginButton = Button(loginPage, text = 'Login', command = verifyLogin,font='Verdana 9 bold',bg='peach puff')
    loginButton.place(x = (pageHeight/2 - buttonWidth/2), y = 350, height = buttonHeight, width = buttonWidth)
    registerButton = Button(loginPage, text = 'Registration', command = loginToRegPage,font='Verdana 9 bold',bg='peach puff')
    registerButton.place(x = (pageHeight/2 - buttonWidth/2), y = 450, height = buttonHeight, width = buttonWidth)
    AdminregisterButton = Button(loginPage, text = 'Admin-Registration(Admin Only)', command = logintoAdminPassword,font='Verdana 9 bold',bg='peach puff')
    AdminregisterButton.place(x = (pageHeight/2 - buttonWidth/2-100), y = 550, height = buttonHeight, width = 350)



## mainPage ##
def mainToAdSearch():
    mainPage.destroy()
    adSearchPageFunction()

def mainToReq():
    mainPage.destroy()
    reqPageFunction()

def mainToService():
    mainPage.destroy()
    servicePageFunction()

def mainToAdFunc():
    mainPage.destroy()
    adFuncPageFunction()

def mainToLogin():
    mainPage.destroy()
    loginPageFunction()

def mainToCustSearch():
    mainPage.destroy()
    custSearchPageFunction()

def mainToServiceReq():
    mainPage.destroy()
    serviceReqPageFunction()

def mainPageFunction():
    global mainPage
    mainPage = Toplevel()
    mainPage.title('Main Page')
    mainPage.geometry(pageGeometry)
    my_label = Label(mainPage, image=pink)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    Label(mainPage,image=oshes2).place(x = (pageHeight/2 - 190), y = 0, height = 100, width = 360)





    if userStatus == 'Admin':
        productSearchButton = Button(mainPage, text = 'Product Search', command = mainToAdSearch,bg='peach puff')
        productSearchButton.place(x = (pageHeight/2 - buttonWidth/2), y = 250, height = buttonHeight, width = buttonWidth)
        requestManagementButton = Button(mainPage, text = 'Request Management', command = mainToReq,bg='peach puff')
        requestManagementButton.place(x = (pageHeight/2 - buttonWidth/2), y = 350, height = buttonHeight, width = buttonWidth)
        serviceManagementButton = Button(mainPage, text = 'Service Management', command = mainToService,bg='peach puff')
        serviceManagementButton.place(x = (pageHeight/2 - buttonWidth/2), y = 450, height = buttonHeight, width = buttonWidth)
        adminFunctionButton = Button(mainPage, text = 'Administrator Functions', command = mainToAdFunc,bg='peach puff')
        adminFunctionButton.place(x = (pageHeight/2 - buttonWidth/2), y = 550, height = buttonHeight, width = buttonWidth)
        logoutButton = Button(mainPage, text = 'Logout', command = mainToLogin,bg='peach puff')
        logoutButton.place(x = (pageHeight/2 - buttonWidth/2), y = 650, height = buttonHeight, width = buttonWidth)

    else:
        productSearchButton = Button(mainPage, text = 'Product Search', command = mainToCustSearch,bg='peach puff')
        productSearchButton.place(x = (pageHeight/2 - buttonWidth/2), y = 250, height = buttonHeight, width = buttonWidth)
        serviceRequestButton = Button(mainPage, text = 'Service Request', command = mainToServiceReq,bg='peach puff')
        serviceRequestButton.place(x = (pageHeight/2 - buttonWidth/2), y = 350, height = buttonHeight, width = buttonWidth)
        logoutButton = Button(mainPage, text = 'Logout', command = mainToLogin,bg='peach puff')
        logoutButton.place(x = (pageHeight/2 - buttonWidth/2), y = 650, height = buttonHeight, width = buttonWidth)

        

## registrationPage ##
def regPageToLoginPage():
    regPage.destroy()
    loginPageFunction()

def regPageFunction():
    global regPage
    regPage = Toplevel()
    regPage.title('Registration Page')
    regPage.geometry(pageGeometry)
    my_label = Label(regPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    Label(regPage, text = 'User ID', font=button_font).place(x = (pageHeight/2 - 200), y = 50, height = buttonHeight, width = buttonWidth)
    userID = StringVar()
    userIDEntry = Entry(regPage, textvariable = userID)
    userIDEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 50, height = buttonHeight, width = buttonWidth)

    Label(regPage, text = 'Password', font=button_font).place(x = (pageHeight/2 - 200), y = 125, height = buttonHeight, width = buttonWidth)
    password = StringVar()
    passwordEntry = Entry(regPage, textvariable = password)
    passwordEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 125, height = buttonHeight, width = buttonWidth)

    Label(regPage, text = 'Name', font=button_font).place(x = (pageHeight/2 - 200), y = 200, height = buttonHeight, width = buttonWidth)
    name = StringVar()
    nameEntry = Entry(regPage, textvariable = name)
    nameEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 200, height = buttonHeight, width = buttonWidth)

    Label(regPage, text = 'Gender', font=button_font).place(x = (pageHeight/2 - 200), y = 275, height = buttonHeight, width = buttonWidth)
    gender = StringVar()
    genders = ["Male", "Female"]
    genderEntry = OptionMenu(regPage, gender, *genders)
    genderEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 275, height = buttonHeight, width = buttonWidth)

    Label(regPage, text = 'Email', font=button_font).place(x = (pageHeight/2 - 200), y = 350, height = buttonHeight, width = buttonWidth)
    email = StringVar()
    emailEntry = Entry(regPage, textvariable = email)
    emailEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 350, height = buttonHeight, width = buttonWidth)

    Label(regPage, text = 'Phone', font=button_font).place(x = (pageHeight/2 - 200), y = 425, height = buttonHeight, width = buttonWidth)
    phone = StringVar()
    phoneEntry = Entry(regPage, textvariable = phone)
    phoneEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 425, height = buttonHeight, width = buttonWidth)

    Label(regPage, text = 'Address', font=button_font).place(x = (pageHeight/2 - 200), y = 500, height = buttonHeight, width = buttonWidth)
    address = StringVar()
    addressEntry = Entry(regPage, textvariable = address)
    addressEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 500, height = buttonHeight, width = buttonWidth)

    def register():
        userIDInput = userIDEntry.get()
        passwordInput = passwordEntry.get()
        nameInput = nameEntry.get()
        genderInput = gender.get()
        emailInput = emailEntry.get()
        phoneInput = phoneEntry.get()
        addressInput = addressEntry.get()

        minimum_character = 4
        max_character = 50
        
        errors = ""
        
        #User ID cannot be blank
        if userIDInput == "":
            errors += "User ID cannot be empty, please fill in an ID \n"
        elif len(userIDInput) < minimum_character or len(userIDInput) > max_character:
            errors += "User ID must be minimum 4 and maximum 50 characters\n"
        elif ifSpace(userIDInput):
            errors += "User ID cannot have spaces \n"

        if passwordInput == "":
            errors += "Password cannot be empty, please fill in a Password \n"
        elif len(passwordInput) < minimum_character or len(passwordInput) > max_character:
            errors += "Password must be minimum 4 and maximum 50 characters \n"
        elif ifSpace(passwordInput):
            errors += "Password cannot have spaces \n"

        if nameInput == "":
            errors += "Name cannot be empty, please fill in a Password \n"
        elif len(nameInput) < minimum_character or len(nameInput) > max_character:
            errors += "Name must be minimum 4 and maximum 50 characters \n"
            

        if genderInput == "":
            errors += "Please fill in your Gender \n"

        if re.search(regex_email, emailInput) == None:
            errors += "Please fill in a valid Email Address \n"
            
                
        if len(phoneInput) == 8 and (phoneInput[0] == "9" or phoneInput[0] == "8" or phoneInput[0] == "6"):
            try:
                phoneInput = int(phoneInput)
            except ValueError:
                errors += "Phone number invalid \n"
        else:
            errors += 'Phone number invalid \n'

        if addressInput == "":
            errors += "Address cannot be empty, please fill in an Address \n"
        elif len(addressInput) < minimum_character or len(addressInput) > max_character:
            errors += "Address must be minimum 4 and maximum 50 characters \n"
        
        
        #check for same userid    
        namecheck="SELECT CustomerID FROM customers;"
        namecheck2="SELECT AdminID FROM Admins;"
        namecheckquery=read_query(connection,namecheck)
        namecheckquery2=read_query(connection,namecheck2)
        for tup in namecheckquery:
            if str(userIDInput)in tup:
                userIDEntry.delete(0, END)
                errors += 'Customer ID already Exists, Please Try Another ID \n'
        for tup in namecheckquery2:
            if str(userIDInput)in tup:
                userIDEntry.delete(0, END)
                errors += 'Customer ID already Exists, Please Try Another ID \n'
                
            
        if errors != "":
            return messagebox.showerror(title = 'Registration Unsuccessful', message = errors)
        else:
            regInput=(str(userIDInput),str(nameInput),str(genderInput),str(emailInput),int(phoneInput),str(addressInput),str(passwordInput))
            regquery="INSERT INTO customers values" +str(regInput)+";"
            execute_query(connection,regquery)
            userIDEntry.delete(0, END)
            passwordEntry.delete(0, END)
            nameEntry.delete(0, END)
            emailEntry.delete(0, END)
            phoneEntry.delete(0, END)
            addressEntry.delete(0, END)
            regPageToLoginPage()
            return messagebox.showinfo(title = 'Registration Successful', message = 'You have successfully registered!')
        

    registerButton = Button(regPage, text = 'Register', font=button_font, command = register,bg='peach puff')
    registerButton.place(x = (pageHeight/2 - buttonWidth/2), y = 575, height = buttonHeight, width = buttonWidth)

    backToLoginPage = Button(regPage, text = 'Back to Login Page', font=button_font, command = regPageToLoginPage,bg='peach puff')
    backToLoginPage.place(x = 1000, y = 575, height = buttonHeight, width = buttonWidth)
    
## Admin Register##
def adregPageToLoginPage():
    adregPage.destroy()
    loginPageFunction()
   
def AdminregPageFunction():
    global adregPage
    adregPage = Toplevel()
    adregPage.title('ADMIN Registration Page')
    adregPage.geometry(pageGeometry)
    my_label = Label(adregPage, font=button_font, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    Label(adregPage, text = 'Admin ID', font=button_font).place(x = (pageHeight/2 - 200), y = 50, height = buttonHeight, width = buttonWidth)
    userID = StringVar()
    userIDEntry = Entry(adregPage, textvariable = userID)
    userIDEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 50, height = buttonHeight, width = buttonWidth)

    Label(adregPage, text = 'Password', font=button_font).place(x = (pageHeight/2 - 200), y = 125, height = buttonHeight, width = buttonWidth)
    password = StringVar()
    passwordEntry = Entry(adregPage, textvariable = password)
    passwordEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 125, height = buttonHeight, width = buttonWidth)

    Label(adregPage, text = 'Name', font=button_font).place(x = (pageHeight/2 - 200), y = 200, height = buttonHeight, width = buttonWidth)
    name = StringVar()
    nameEntry = Entry(adregPage, textvariable = name)
    nameEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 200, height = buttonHeight, width = buttonWidth)

    Label(adregPage, text = 'Gender', font=button_font).place(x = (pageHeight/2 - 200), y = 275, height = buttonHeight, width = buttonWidth)
    gender = StringVar()
    genders = ["Male", "Female"]
    genderEntry = OptionMenu(adregPage, gender, *genders)
    genderEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 275, height = buttonHeight, width = buttonWidth)

  

    Label(adregPage, text = 'Phone', font=button_font).place(x = (pageHeight/2 - 200), y = 350, height = buttonHeight, width = buttonWidth)
    phone = StringVar()
    phoneEntry = Entry(adregPage, textvariable = phone)
    phoneEntry.place(x = (pageHeight/2 - buttonWidth/2), y = 350, height = buttonHeight, width = buttonWidth)

    def register():
        adminIDInput = userIDEntry.get()
        passwordInput = passwordEntry.get()
        nameInput = nameEntry.get()
        genderInput = gender.get()
        phoneInput = phoneEntry.get()

        errors = ""

        minimum_character = 4
        max_character = 50
        
        
        #User ID cannot be blank
        if adminIDInput == "":
            errors += "Admin ID cannot be empty, please fill in an ID \n"
        elif len(adminIDInput) < minimum_character or len(adminIDInput) > max_character:
            errors += "Admin ID must be minimum 4 and maximum 50 characters\n"
        elif ifSpace(adminIDInput):
            errors += "Admin ID cannot have spaces \n"

        if passwordInput == "":
            errors += "Password cannot be empty, please fill in a Password \n"
        elif len(passwordInput) < minimum_character or len(passwordInput) > max_character:
            errors += "Password must be minimum 4 and maximum 50 characters \n"
        elif ifSpace(passwordInput):
            errors += "Password cannot have spaces \n"

        if nameInput == "":
            errors += "Name cannot be empty, please fill in a Password \n"
        elif len(nameInput) < minimum_character or len(nameInput) > max_character:
            errors += "Name must be minimum 4 and maximum 50 characters \n"

        if genderInput == "":
            errors += "Please fill in your Gender \n"
            
                
        if len(phoneInput) == 8 and (phoneInput[0] != "9" or phoneInput[0] != '8' or phoneInput[0] != '6'):
            try:
                phoneInput = int(phoneInput)
            except ValueError:
                errors += "Phone number invalid \n"
        else:
            errors += 'Phone number invalid \n'
        
    

        namecheck="SELECT CustomerID FROM customers;"
        namecheck2="SELECT AdminID FROM Admins;"
        namecheckquery=read_query(connection,namecheck)
        namecheckquery2=read_query(connection,namecheck2)
        for tup in namecheckquery:
            if str(adminIDInput)in tup:
                userIDEntry.delete(0, END)
                errors += 'ID already Exists, Please Try Another ID \n'
        for tup in namecheckquery2:
            if str(adminIDInput)in tup:
                userIDEntry.delete(0, END)
                errors += 'ID already Exists, Please Try Another ID \n'
            
        #other input verification

        if errors != "":
            return messagebox.showerror(title = 'Registration Unsuccessful', message = errors)

        else:
            regInput=(str(adminIDInput),str(nameInput),str(genderInput),int(phoneInput),str(passwordInput))
            regquery="INSERT INTO admins values" +str(regInput)+";"
            execute_query(connection,regquery)
            userIDEntry.delete(0, END)
            passwordEntry.delete(0, END)
            nameEntry.delete(0, END)
            phoneEntry.delete(0, END)
            adregPageToLoginPage()
            return messagebox.showinfo(title = 'Registration Successful', message = 'You have successfully registered!')
        
    registerButton = Button(adregPage, text = 'Register', font=button_font, command = register,bg='peach puff')
    registerButton.place(x = (pageHeight/2 - buttonWidth/2), y = 450, height = buttonHeight, width = buttonWidth)

    backToLoginPage = Button(adregPage, text = 'Back to Login Page', font=button_font, command = adregPageToLoginPage,bg='peach puff')
    backToLoginPage.place(x = 1000, y = 575, height = buttonHeight, width = buttonWidth)

## customerSearchPage ##
def custSearchPageToCustResultPage():
    custSearchPage.destroy()
    custResultPageFunction()

def custSearchPageToMainPage():
    custSearchPage.destroy()
    mainPageFunction()

def custSearchPageFunction():
    global custSearchPage
    custSearchPage = Toplevel()
    custSearchPage.title('Customer Search Page')
    custSearchPage.geometry(pageGeometry)
    my_label = Label(custSearchPage, image=rainbow, font=button_font)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    top_y = 25
    spacing = 60;
    ##Simple Search Buttons##
    Label(custSearchPage, text = 'Simple Search', font=button_font).place(x = (pageHeight/3 - buttonWidth/2), y = top_y, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Category', font=button_font).place(x = (pageHeight/3 - 200), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)
    category_S = StringVar()
    categories = [""] + getJsonValues('Category')
    #run query to fetch categories
    categoryEntry_S = OptionMenu(custSearchPage, category_S, *categories)
    categoryEntry_S.place(x = (pageHeight/3 - buttonWidth/2), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Model', font=button_font).place(x = (pageHeight/3 - 200), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)
    model_S = StringVar()
    models = [""] + getJsonValues('Model')
    #run query to fetch models
    modelEntry_S = OptionMenu(custSearchPage, model_S, *models)
    modelEntry_S.place(x = (pageHeight/3 - buttonWidth/2), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)


    ##Advanced Search Buttons##
    Label(custSearchPage, text = 'Advanced Search', font=button_font).place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Category', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)
    category_A = StringVar()
    category_A.set("")
    categories = [""] + getJsonValues('Category')
    #run query to fetch categories
    categoryEntry_A = OptionMenu(custSearchPage, category_A, *categories)
    categoryEntry_A.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Model', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)
    model_A = StringVar()
    model_A.set("")
    models = [""] + getJsonValues('Model')
    #run query to fetch models
    modelEntry_A = OptionMenu(custSearchPage, model_A, *models)
    modelEntry_A.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)


    Label(custSearchPage, text = 'Price', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*3, height = buttonHeight, width = buttonWidth)
    price = StringVar()
    #run query to fetch prices
    price.set("")
    price_values = [""] + getJsonValues('Price ($)')
    priceEntry = OptionMenu(custSearchPage, price, *price_values)
    priceEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*3, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Warranty', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*4, height = buttonHeight, width = buttonWidth)
    warranty = StringVar()
    #run query to fetch warranty
    warranty_values =[""] + getJsonValues('Warranty (months)')
    warrantyEntry = OptionMenu(custSearchPage, warranty, *warranty_values)
    warrantyEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*4, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Colour', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*5, height = buttonHeight, width = buttonWidth)
    colour = StringVar()
    #run query to fetch colours
    colour_values =[""] + getJsonValues('Color')
    colourEntry = OptionMenu(custSearchPage, colour, *colour_values)
    colourEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*5, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Factory', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*6, height = buttonHeight, width = buttonWidth)
    factory = StringVar()
    #run query to fetch factories
    factory_values =[""] + getJsonValues('Factory')
    factoryEntry = OptionMenu(custSearchPage, factory, *factory_values)
    factoryEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*6, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Production Year', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*7, height = buttonHeight, width = buttonWidth-20)
    productionYear = StringVar()
    #run query to fetch productionYears
    productionYear_values =[""] + getJsonValues('ProductionYear')
    productionYearEntry = OptionMenu(custSearchPage, productionYear, *productionYear_values)
    productionYearEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*7, height = buttonHeight, width = buttonWidth)

    Label(custSearchPage, text = 'Power Supply', font=button_font).place(x = (pageHeight/3*2 - 200), y = top_y + spacing*8, height = buttonHeight, width = buttonWidth)
    powerSupply = StringVar()
    #run query to fetch productionYears
    powerSupply_values =[""] + getJsonValues('PowerSupply')
    powerSupplyEntry = OptionMenu(custSearchPage, powerSupply, *powerSupply_values)
    powerSupplyEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*8, height = buttonHeight, width = buttonWidth)

    def executeSimpleSearch():
        global searchResult
        global checkSearch
        checkSearch = "Simple"
        categoryInput_S = category_S.get()
        modelInput_S = model_S.get()

        if categoryInput_S != "" and modelInput_S != "":
            category_S.set("")
            model_S.set("")
            return messagebox.showerror(title = 'Search Error',\
                                        message = 'Please key in EITHER Category or Model')
        elif categoryInput_S == "" and modelInput_S == "":
            return messagebox.showerror(title = 'Search Error',\
                                        message = 'No input: Please key in EITHER Category or Model')
        else:
            if categoryInput_S != "":
                searchResult = simpleSearchC(categoryInput_S)
            else:
                searchResult = simpleSearchC(modelInput_S)
 

            
        custSearchPageToCustResultPage()

    def executeAdvSearch():
        global searchResult
        global checkSearch
        checkSearch = "Advanced"
        categoryInput_A = category_A.get()
        modelInput_A = model_A.get()
        priceInput = price.get()
        warrantyInput = warranty.get()
        colourInput = colour.get()
        factoryInput = factory.get()
        productionYearInput = productionYear.get()
        powerSupplyInput = powerSupply.get()

        if warrantyInput != "":
            warrantyInput = int(warrantyInput)
        if priceInput != "":
            priceInput = int(priceInput)
            
        searchResult = advSearchC(priceInput, warrantyInput, categoryInput_A, modelInput_A, \
                                  colourInput, factoryInput, productionYearInput, powerSupplyInput)

        if searchResult == []:
            messagebox.showerror(title = 'No Such Item',\
                                        message = 'No Such item available with the above filters')
        else:
            custSearchPageToCustResultPage()
            

    executeSimpleSearchButton = Button(custSearchPage, text = 'Simple Search', command = executeSimpleSearch,bg='peach puff', font=button_font)
    executeSimpleSearchButton.place(x = (pageHeight/3 - buttonWidth/2), y = top_y + spacing*9, height = buttonHeight, width = buttonWidth)

    executeAdvSearchButton = Button(custSearchPage, text = 'Advanced Search', command = executeAdvSearch,bg='peach puff', font=button_font)
    executeAdvSearchButton.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*9, height = buttonHeight, width = buttonWidth)

    backToMainPageButton = Button(custSearchPage, text = 'Back to Main Page', command = custSearchPageToMainPage,bg='peach puff', font=button_font)
    backToMainPageButton.place(x = 1000, y = top_y + spacing*9, height = buttonHeight, width = buttonWidth)


## customer result page ##
def purchasePageToMainPage():
    custResultPage.destroy()
    confirmPurchasePage.destroy()
    global purchaseWindow
    purchaseWindow = False
    mainPageFunction()


def custResultPageToCustSearchPage():
    custResultPage.destroy()
    custSearchPageFunction()

def custResultPageFunction():
    global custResultPage
    custResultPage = Toplevel()
    custResultPage.title('Customer Result Page')
    custResultPage.geometry(pageGeometry)
    my_label = Label(custResultPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    global purchaseWindow
    purchaseWindow = False

    
    if checkSearch == "Simple":
        #load simple search results
        searchColumns = ('Category', 'Model', 'Price ($)', 'Warranty (months)', \
                                  'Inventory', 'Purchase Qty')
        searchTable = ttk.Treeview(custResultPage, columns= searchColumns, show='headings',\
                                   selectmode = "extended")
       
        searchTable.heading('Category', text = 'Category', anchor = CENTER)
        searchTable.column('Category', width = 120)
        searchTable.heading('Model', text = 'Model', anchor = CENTER)
        searchTable.heading('Price ($)', text = 'Price ($)', anchor = CENTER)
        searchTable.column('Price ($)', width = 60)
        searchTable.heading('Warranty (months)', text = 'Warranty (months)', anchor = CENTER)
        searchTable.column('Warranty (months)', width = 120)
        searchTable.heading('Inventory', text = 'Inventory', anchor = CENTER)
        searchTable.column('Inventory', width = 120)
        searchTable.heading('Purchase Qty', text = 'Purchase Quantity', anchor = CENTER)
        searchTable.column('Purchase Qty', width = 120)
        
        searchTable.tag_configure('oddrow',background = 'blue')

        #Center Values
        for column in searchColumns:
            searchTable.column(column, anchor = CENTER)

        for result in searchResult:
            resultTuple = ()
            for column in searchColumns[:-1]:           
                resultTuple += (result[column],)
            searchTable.insert(parent = '', index = searchResult.index(result), values = resultTuple + (0, ))
        searchTable.pack()
        
        #style = ttk.Style()
        #style.theme_use('default')
        #style.map("Treeview")
        #display search results
        #run query using global variables

    else:
        #load advanced search results

        searchColumns = ('Category', 'Model', 'Price ($)', 'Warranty (months)', \
                         'Color', 'Factory', 'ProductionYear', 'PowerSupply', 'Inventory', 'Purchase Qty')
        searchTable = ttk.Treeview(custResultPage, columns = searchColumns, show = 'headings')
        searchTable.heading('Category', text = 'Category', anchor = CENTER)
        searchTable.column('Category', width = 120)
        searchTable.heading('Model', text = 'Model', anchor = CENTER)
        searchTable.heading('Price ($)', text = 'Price ($)', anchor = CENTER)
        searchTable.column('Price ($)', width = 60)
        searchTable.heading('Warranty (months)', text = 'Warranty (months)', anchor = CENTER)
        searchTable.column('Warranty (months)', width = 120)
        searchTable.heading('Color', text = 'Color', anchor = CENTER)
        searchTable.column('Color', width = 120)
        searchTable.heading('Factory', text = 'Factory', anchor = CENTER)
        searchTable.column('Factory', width = 120)
        searchTable.heading('ProductionYear', text = 'Production Year', anchor = CENTER)
        searchTable.column('ProductionYear', width = 120)
        searchTable.heading('PowerSupply', text = 'Power Supply', anchor = CENTER)
        searchTable.column('PowerSupply', width = 120)
        searchTable.heading('Inventory', text = 'Inventory', anchor = CENTER)
        searchTable.column('Inventory', width = 120)
        searchTable.heading('Purchase Qty', text = 'Purchase Quantity', anchor = CENTER)
        searchTable.column('Purchase Qty', width = 120)

        #Center Values
        for column in searchColumns:
            searchTable.column(column, anchor = CENTER)

        finalResult ={}
        for result in searchResult:
            resultTuple = ()
            for column in searchColumns[:-2]:
                resultTuple += (result[column],)
            if resultTuple not in finalResult:
                finalResult[resultTuple] = 1
            else:
                finalResult[resultTuple] += 1
        finalList = []
        for k, v in finalResult.items():
            finalList.append(k + (v, ))
        for entry in finalList:
            searchTable.insert(parent='', index = finalList.index(entry), values = entry + (0,))
            
    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")
    searchTable.pack()
        
    def addPurchase():
        row = searchTable.selection()
        if row == ():
            return messagebox.showwarning(title = 'Warning', message = 'Select items to be added to Purchases')
        final = 0
        for i in row:
            current_value = searchTable.item(i)['values'][-1]
            inventory_value = searchTable.item(i)['values'][-2]
            if inventory_value <= current_value:
                final += 1
                
        if final > 0:
            return messagebox.showerror(title = 'Error', message = 'One of your selected item(s) has insufficient stock')
        else:
            for i in row:
                current_value = searchTable.item(i)['values'][-1]
                inventory_value = searchTable.item(i)['values'][-2]            
                searchTable.set(i, column = 'Purchase Qty', value = current_value + 1)
            

    def minusPurchase():
        row = searchTable.selection()
        if row == ():
            return messagebox.showwarning(title = 'Warning', message = 'Select items to be dropped from Purchases')
        final=0
        for i in row:
            current_value = searchTable.item(i)['values'][-1]
            inventory_value = searchTable.item(i)['values'][-2]
            if current_value == 0:
                final+=1
        if final>0:
            return messagebox.showerror(title = 'Error', message = ' One of your selected item(s) purchase quantity is already 0')

        else:
            for i in row:
                current_value = searchTable.item(i)['values'][-1]
                inventory_value = searchTable.item(i)['values'][-2]            
                searchTable.set(i, column = 'Purchase Qty', value = current_value - 1)
            
    xscrollbar = ttk.Scrollbar(custResultPage, orient="horizontal", command=searchTable.xview)

    xscrollbar.pack(side="bottom", fill="x")

    addPurchaseButton = Button(custResultPage, text = 'Add Items to Purchase(+)', command = addPurchase,bg='peach puff')
    addPurchaseButton.place(x = (pageHeight/2 - buttonWidth/2), y = 350, height = buttonHeight, width = buttonWidth)

    minusPurchaseButton = Button(custResultPage, text = 'Drop Items to Purchase(-) ', command = minusPurchase,bg='peach puff')
    minusPurchaseButton.place(x = (pageHeight/2 - buttonWidth/2), y = 450, height = buttonHeight, width = buttonWidth)



    def makePurchase():
        row = searchTable.get_children()

        result = []
        for i in row:
            get_purchase_qty = searchTable.item(i)['values'][-1]
            if get_purchase_qty > 0:
                result.append(searchTable.item(i)['values'])
        global purchaseList
        purchaseList = result


        global purchaseWindow
        if result != []:
            if not purchaseWindow:
                confirmPurchase()

                


            else:
                return messagebox.showerror(title = 'Error',\
                                        message = 'Multiple Purchase Windows Opened')
        else:
            return messagebox.showerror(title = 'Error',\
                                        message = 'Please select at least one item to be purchased')
  

    def cancelPurchase():
        global purchaseWindow
        purchaseWindow = False
        confirmPurchasePage.destroy()

    def updatePurchase():
        itemIdList = []
        if checkSearch == "Simple":
            for item in purchaseList:
                result = read_query(connection, "SELECT ItemID FROM items WHERE category='%s' AND model='%s' AND purchasestatus='Unsold' LIMIT %d;" % (item[0], item[1], item[-1]))
                for i in result:
                    itemIdList.append(i[0])
        else:
            for item in purchaseList:
                result = read_query(connection, "SELECT ItemID FROM items WHERE category='%s' AND model='%s' AND color='%s' AND "
                                    "factory='%s' AND productionyear='%s' AND powersupply='%s' AND purchasestatus='Unsold' LIMIT %d;"
                                    % (item[0], item[1], item[4], item[5], item[6], item[7], item[-1]))
                for i in result:
                    itemIdList.append(i[0])
        for i in itemIdList:
            today = date.today()
            d1 = today.strftime('%Y-%m-%d %H:%M:%S')
            execute_query(connection, "UPDATE items SET purchasestatus='Sold' , customerID='%s' , purchasedate='%s' WHERE itemID='%s';" % (CurrentUserID, d1, i))
        #update mongodb
        mongoUpdatePurchase(itemIdList)
        messagebox.showinfo(title='Success',message='Purchase is Successful!')
        purchasePageToMainPage()
    
        pass
        

    def confirmPurchase():
        global confirmPurchasePage

        global purchaseWindow
        purchaseWindow = True

        confirmPurchasePage = Toplevel()
        confirmPurchasePage.title('Confirm Purchase')
        confirmPurchasePage.geometry('400x380')
        Label(confirmPurchasePage, text = 'Confirm Purchase?',bg='gold').place(x = 75, y = 10, height = 50, width = 250)
        my_label = Label(confirmPurchasePage, image=pink)
        my_label.place(x=0,y=0,relwidth=1,relheight=1)

        #display total items bought and total cost
        count_items = 0
        price_items = 0

        if checkSearch == 'Simple':
            for item in purchaseList:
                count_items += item[5]
                price_items += item[5]*item[2]
        else:
            for item in purchaseList:
                count_items += item[9]
                price_items += item[9]*item[2]
            
        
        Label(confirmPurchasePage, text = 'Total Items Purchased: ' + str(count_items)).place(x = 75, y = 100, height = 50, width = 250)
        Label(confirmPurchasePage, text = 'Total Price: $' + str(price_items)).place(x = 75, y = 150, height = 50, width = 250)

        yesButton = Button(confirmPurchasePage, text = 'Yes', command = updatePurchase,bg='peach puff')
        yesButton.place(x = 100, y =300 , height = buttonHeight, width = 50)

        noButton = Button(confirmPurchasePage, text = 'No', command = cancelPurchase,bg='peach puff')
        noButton.place(x = 225, y = 300 , height = buttonHeight, width = 50)
    

    

    makePurchaseButton = Button(custResultPage, text = 'Make Purchase', command = makePurchase,bg='peach puff')
    makePurchaseButton.place(x = (pageHeight/2 - buttonWidth/2), y = 550, height = buttonHeight, width = buttonWidth)
            
    newSearchButton = Button(custResultPage, text = 'New Search', command = custResultPageToCustSearchPage,bg='peach puff')
    newSearchButton.place(x = (pageHeight/2 - buttonWidth/2), y = 650, height = buttonHeight, width = buttonWidth)


## serviceReqPage ##
def serviceReqPageToMainPage():
    serviceReqPage.destroy()
    mainPageFunction()

def refreshServiceReqPage():
    serviceReqPage.destroy()
    serviceReqPageFunction()

def serviceReqPageFunction():
    global requestWindow
    requestWindow = False
    global serviceReqPage
    serviceReqPage = Toplevel()
    serviceReqPage.title('Service Request Page')
    serviceReqPage.geometry(pageGeometry)
    my_label = Label(serviceReqPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    
    result_columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8','#9','#10', '#11', '#12')
    result_table = ttk.Treeview(serviceReqPage, columns=result_columns, show='headings')

  
    result_table.heading('#1', text='ItemID')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='Request Status')
    result_table.heading('#3', text='Service Status')
    result_table.heading('#4', text='Submission Date')
    result_table.column('#4', width = 120)
    result_table.heading('#5', text='Category')
    result_table.column('#5', width = 120)
    result_table.heading('#6', text='Model')
    result_table.heading('#7', text='Color')
    result_table.column('#7', width = 120)
    result_table.heading('#8', text='Factory')
    result_table.column('#8', width = 120)
    result_table.heading('#9', text='Power Supply')
    result_table.column('#9', width = 120)
    result_table.heading('#10', text='Production Year')
    result_table.column('#10', width = 120)
    result_table.heading('#11', text='Request ID')
    result_table.column('#11', width = 120)
    result_table.heading('#12', text='Purchase Date')
    result_table.column('#12', width = 120)

    
    result_table.pack()
    
    querycheck="SELECT * FROM items \
    WHERE CustomerID = '%s' \
    GROUP BY ItemID ORDER BY PurchaseDate DESC;" % (CurrentUserID)
    items_bought_table = read_query(connection,querycheck)
    items_id_table = []
    for entry in items_bought_table:
        items_id_table.append(entry[0])

    request_status_table = []
    for i in items_id_table:
        next_status = read_query(connection, "SELECT requestid, requeststatus, submissiondate FROM servicerequests WHERE itemid='%s';" % (i))
        if len(next_status) == 0:
            request_status_table.append(['','',''])
        else:
            request_status_table.append(next_status[-1])
    for i in range(len(items_bought_table)):
        result_table.insert(parent='', index=i,
                            values=(items_bought_table[i][0], request_status_table[i][1], items_bought_table[i][8], request_status_table[i][2], items_bought_table[i][1],
                                    items_bought_table[i][7], items_bought_table[i][2], items_bought_table[i][3], items_bought_table[i][4], items_bought_table[i][6],
                                    request_status_table[i][0], items_bought_table[i][-1]))
        
    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")
    result_table.pack()


    for column in result_columns:
            result_table.column(column, anchor = CENTER)

            
    def confirmRequest():
        row = result_table.selection()


        if len(row)==0:
            return messagebox.showerror(title = 'No Selection', message = 'Please Select At Least 1 Item')
        else:
            global requestWindow
            if not requestWindow:
                global confirmRequestPage
                confirmRequestPage = Toplevel()
                confirmRequestPage.title('Confirm Request')
                confirmRequestPage.geometry('260x180')
                Label(confirmRequestPage, text = 'Confirm Request?').place(x = 10, y = 10, height = 50, width = 250)

         
                requestWindow = True

                yesButton = Button(confirmRequestPage, text = 'Yes', command = createRequest,bg='peach puff')
                yesButton.place(x = 30, y =110 , height = buttonHeight, width = 50)

                noButton = Button(confirmRequestPage, text = 'No', command = noRequest,bg='peach puff')
                noButton.place(x = 150, y =110 , height = buttonHeight, width = 50)
            else:
                return messagebox.showerror(title = 'Error', message = 'Multiple Request Windows Opened')

            
    def noRequest():
        confirmRequestPage.destroy()
        global requestWindow
        requestWindow = False


    
    def createRequest():
        row = result_table.selection()
        doublecheck=[]


        for i in row:
            ItemID = result_table.item(i)['values'][0]
            checkitemID="SELECT RequestID, RequestStatus FROM servicerequests WHERE itemID='%s';"%(ItemID)
            #Check if ITEMID in servicRequests:
            #should we select only one item?
            check=read_query(connection,checkitemID)
            if len(check)!=0:
                if check[-1][1] != 'Cancelled' and check[-1][1] != 'Completed':
                    doublecheck.append(ItemID)
        items=''
        if len(doublecheck)>0:
            for item in doublecheck:
                items+=str(item)+','
            confirmRequestPage.destroy()
            return messagebox.showerror(title = 'Item Servicing Error',\
                                            message = "Service has already been sent for items'%s'Please Unselect Items"%(items))
        else:
            expired=[]
            notexpired=[]
            for i in row:
                ItemID = result_table.item(i)['values'][0]
                PDate = result_table.item(i)['values'][-1]
                cat= result_table.item(i)['values'][4]
                model= result_table.item(i)['values'][5]
                date_time_obj = datetime. strptime(PDate,'%Y-%m-%d')
                newdate=date_time_obj+relativedelta(months=+10)


                ###Manually Change Date###
                today=datetime.strptime(date_input,'%Y-%m-%d')
                #if currentdate>new date, free warranty has expired and payment is needed
                if today>newdate: 
                    RequestStatus="Submitted and Waiting for Payment"
                    expired.append(ItemID)
                    execute_query(connection,"UPDATE items SET Servicestatus='' WHERE itemID='%s';" % (ItemID))
                #else, no payment is needed and request is submitted straight
                else:
                    RequestStatus="Submitted"
                    notexpired.append(ItemID)
                    execute_query(connection,"UPDATE items SET Servicestatus='Waiting for Approval' WHERE itemID='%s';" % (ItemID))
                #Insert new row into servicce request-- Request ID is auto filled(auto increment)
                next_query = "INSERT INTO ServiceRequests(ItemID,CustomerID,SubmissionDate,RequestStatus) VALUES( '%s','%s','%s','%s');"%(str(ItemID),str(CurrentUserID),str(d1),str(RequestStatus))
                execute_query(connection,next_query)
                #Insert into ServiceFee
                if RequestStatus=="Submitted and Waiting for Payment":
                    get_request="SELECT requestID FROM ServiceRequests WHERE ItemID='%s' AND CustomerID='%s';"%(str(ItemID),str(CurrentUserID))
                    request_id=read_query(connection,get_request)
                    req=request_id[-1][0]
                    #fee= $40 + 20 percent of item cost
                    get_itemcost="SELECT cost FROM products WHERE Category='%s' AND Model='%s';"%(cat,model)
                    itemcost=read_query(connection,get_itemcost)
                    cost=itemcost[0][0]
                    Fee=40+(cost*0.2)
                    
                    servicefeeq="INSERT INTO servicefee Values('%s',%f,'%s',%s);"%(str(req),Fee,str(CurrentUserID), 'NULL')
                
                    execute_query(connection,servicefeeq)
        exp=''
        notexp=''
        for item in expired:
            exp+=str(item)+','
        for item in notexpired:
            notexp+=str(item)+','
        confirmRequestPage.destroy()
        refreshServiceReqPage()
        return messagebox.showinfo(title = 'Request Successful', message = "Request Submitted for items:'%s',Please Make Payment for items:'%s';"%(str(notexp),str(exp)))    

    def cancelRequest():
        row = result_table.selection()
        global requestWindow
        if len(row)==0:
            return messagebox.showerror(title = 'No Selection', message = 'Please Select At Least 1 Item')
                    
        else:
            if not requestWindow:
                global confirmCancelPage
                confirmCancelPage = Toplevel()
                confirmCancelPage.title('Confirm Cancel Request')
                confirmCancelPage.geometry('260x180')
                Label(confirmCancelPage, text = 'Confirm Cancel Request?').place(x = 10, y = 10, height = 50, width = 250)
                requestWindow = True

                yesButton = Button(confirmCancelPage, text = 'Yes', command = deleteRequest,bg='peach puff')
                yesButton.place(x = 30, y =110 , height = buttonHeight, width = 50)

                noButton = Button(confirmCancelPage, text = 'No', command = noCancel,bg='peach puff')
                noButton.place(x = 150, y =110 , height = buttonHeight, width = 50)
            else:
                return messagebox.showerror(title = 'Error', message = 'Multiple Request Windows Opened')
                

    def noCancel():
        confirmCancelPage.destroy()
        global requestWindow
        requestWindow = False

    def deleteRequest():
        row = result_table.selection()
        success_cancel = ""
        for i in row:
            ItemID = result_table.item(i)['values'][0]
            currentReqStatus = result_table.item(i)['values'][1]
            if currentReqStatus == 'Approved' or currentReqStatus == 'Completed' or currentReqStatus == 'Cancelled' or currentReqStatus == 'None':
                noCancel()
                return messagebox.showerror(title = 'Error',
                                            message = "Request for '%s' is approved, completed, has no request made or is already cancelled! Please unselect '%s' to proceed." % (ItemID, ItemID))

        for i in row:
            ItemID = result_table.item(i)['values'][0]
            reqID = result_table.item(i)['values'][10]
            currentReqStatus = result_table.item(i)['values'][1]
            if currentReqStatus == 'Submitted and Waiting for Payment':
                execute_query(connection, "DELETE FROM servicefees WHERE requestid='%s';" % (reqID))
            execute_query(connection, "UPDATE items SET Servicestatus='' WHERE itemID='%s';" % (ItemID))
            execute_query(connection, "UPDATE servicerequests SET requeststatus='Cancelled' WHERE requestid='%s';" % (reqID))
            success_cancel += "'%s' , " % (ItemID)
        confirmCancelPage.destroy()
        refreshServiceReqPage()
        return messagebox.showinfo(title='Success', message="Items %s have been successfully cancelled!" % (success_cancel))
                              
                
        
    CreateRequestButton = Button(serviceReqPage, text = 'Create Service Request', command = confirmRequest,bg='peach puff')
    CreateRequestButton.place(x = (pageHeight/2 - buttonWidth/2), y = 340, height = buttonHeight, width = buttonWidth)

    cancelRequestButton = Button(serviceReqPage, text = 'Cancel Service Request', command = cancelRequest,bg='peach puff')
    cancelRequestButton.place(x = (pageHeight/2 - buttonWidth/2), y = 410, height = buttonHeight, width = buttonWidth)
    
    PayRequestButton = Button(serviceReqPage, text = 'View Outstanding Fees', command = serviceReqPageToReqPaymentPage,bg='peach puff')
    PayRequestButton.place(x = (pageHeight/2 - buttonWidth/2), y = 480, height = buttonHeight, width = buttonWidth)
    
    backToMainPageButton = Button(serviceReqPage, text = 'Back to Main Page', command = serviceReqPageToMainPage,bg='peach puff')
    backToMainPageButton.place(x = (pageHeight/2 - buttonWidth/2), y = 550, height = buttonHeight, width = buttonWidth)

    xscrollbar = ttk.Scrollbar(serviceReqPage, orient="horizontal", command=result_table.xview)
    xscrollbar.pack(side="bottom", fill="x")
def serviceReqPageToReqPaymentPage():
    serviceReqPage.destroy()
    reqPaymentPageFunction()


## reqPaymentPage ##
def backToServiceReqPage():
    reqPaymentPage.destroy()
    serviceReqPageFunction()

def refreshReqPaymentPage():
    reqPaymentPage.destroy()
    reqPaymentPageFunction()
    
def reqPaymentPageFunction():
    
    global reqPaymentPage
    reqPaymentPage = Toplevel()
    reqPaymentPage.title('Request Payment Page')
    reqPaymentPage.geometry(pageGeometry)
    my_label = Label(reqPaymentPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    
    result_columns = ('#1', '#2', '#3', '#4', '#5')
    result_table = ttk.Treeview(reqPaymentPage, columns=result_columns, show='headings')
    result_table.heading('#1', text='Fee')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='RequestID')
    result_table.column('#2', width = 120)
    result_table.heading('#3', text='ItemID')
    result_table.column('#3', width = 60)
    result_table.heading('#4', text='Submission Date')
    result_table.column('#4', width = 120)
    result_table.heading('#5', text='Request Status')
    result_table.pack()

    xscrollbar = ttk.Scrollbar(reqPaymentPage, orient="horizontal", command=result_table.xview)
    xscrollbar.pack(side="bottom", fill="x")

    unpaid_table = read_query(connection, "SELECT F.Fee, S.RequestID, S.ItemID, S.SubmissionDate, S.RequestStatus "
                              "FROM servicerequests S LEFT JOIN servicefee F ON "
                              "S.RequestID = F.RequestID "
                              "WHERE S.CustomerID='%s' "
                              "AND S.RequestStatus='Submitted and Waiting for Payment';" % (CurrentUserID))

    for i in range(len(unpaid_table)):
        result_table.insert(parent='', index=i,
                            values=(float(unpaid_table[i][0]), unpaid_table[i][1], unpaid_table[i][2], unpaid_table[i][3],
                                    unpaid_table[i][4]))
    
    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")
    result_table.pack()

    for column in result_columns:
        result_table.column(column, anchor = CENTER)

    def makePayment():
        try:
            today = date.today()
            d1 = today.strftime('%Y-%m-%d')
            row = result_table.selection()
            total_fee = 0
            if len(row) == 0:
                return messagebox.showerror(title='Error', message='Please Select an Item to Pay')
            for i in row:
                next_fee = float(result_table.item(i)['values'][0])
                total_fee += next_fee
                reqID = result_table.item(i)['values'][1]
                itemID = result_table.item(i)['values'][2]
                execute_query(connection, "UPDATE servicerequests SET requeststatus='In Progress' WHERE requestid='%s'" % (reqID))
                execute_query(connection, "UPDATE items SET servicestatus='Waiting for Approval' WHERE itemid='%s'" % (itemID))
                execute_query(connection, "UPDATE servicefee SET paymentdate='%s' WHERE requestid='%s'" % (d1, reqID))
            refreshReqPaymentPage()
            return messagebox.showinfo(title = 'Success', message = "Payment for $'%.2f' successful!" % (total_fee))
        except Exception as e:
            print(e)
            return messagebox.showerror(title = 'Error', message = 'Unable to make payment!')
        

    makePaymentButton = Button(reqPaymentPage, text='Make Payment', command=makePayment,bg='peach puff')
    makePaymentButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)

    
    backToserviceReqPageButton = Button(reqPaymentPage, text='Back to Service Request', command=backToServiceReqPage,bg='peach puff')
    backToserviceReqPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=650, height=buttonHeight, width=buttonWidth)








## admin search page ##
def adSearchPageToAdResultPage():
    adSearchPage.destroy()
    adResultPageFunction()

def adSearchPageToMainPage():
    adSearchPage.destroy()
    mainPageFunction()

def adSearchPageFunction():
    global adSearchPage
    adSearchPage = Toplevel()
    adSearchPage.title('Admin Search Page')
    adSearchPage.geometry(pageGeometry)
    my_label = Label(adSearchPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    top_y = 25
    spacing = 60;
    
    ##Simple Search Buttons##
    Label(adSearchPage, text = 'Simple').place(x = (pageHeight/3 - buttonWidth/2), y = top_y, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Category').place(x = (pageHeight/3 - 200), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)
    category_S = StringVar()
    categories = [""] + getJsonValues('Category')
    #run query to fetch categories
    categoryEntry_S = OptionMenu(adSearchPage, category_S, *categories)
    categoryEntry_S.place(x = (pageHeight/3 - buttonWidth/2), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Model').place(x = (pageHeight/3 - 200), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)
    model_S = StringVar()
    models = [""] + getJsonValues('Model')
    #run query to fetch models
    modelEntry_S = OptionMenu(adSearchPage, model_S, *models)
    modelEntry_S.place(x = (pageHeight/3 - buttonWidth/2), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)


    ##Advanced Search Buttons##
    Label(adSearchPage, text = 'Advanced').place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Category').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)
    category_A = StringVar()
    category_A.set("")
    categories = [""] + getJsonValues('Category')
    #run query to fetch categories
    categoryEntry_A = OptionMenu(adSearchPage, category_A, *categories)
    categoryEntry_A.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*1, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Model').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)
    model_A = StringVar()
    model_A.set("")
    models = [""] + getJsonValues('Model')
    #run query to fetch models
    modelEntry_A = OptionMenu(adSearchPage, model_A, *models)
    modelEntry_A.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*2, height = buttonHeight, width = buttonWidth)


    Label(adSearchPage, text = 'Price').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*3, height = buttonHeight, width = buttonWidth)
    price = StringVar()
    #run query to fetch prices
    price.set("")
    price_values =[""] + getJsonValues('Price ($)')
    priceEntry = OptionMenu(adSearchPage, price, *price_values)
    priceEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*3, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Warranty').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*4, height = buttonHeight, width = buttonWidth)
    warranty = StringVar()
    #run query to fetch warranty
    warranty_values =[""] + getJsonValues('Warranty (months)')
    warrantyEntry = OptionMenu(adSearchPage, warranty, *warranty_values)
    warrantyEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*4, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Colour').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*5, height = buttonHeight, width = buttonWidth)
    colour = StringVar()
    #run query to fetch colours
    colour_values =[""] + getJsonValues('Color')
    colourEntry = OptionMenu(adSearchPage, colour, *colour_values)
    colourEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*5, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Factory').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*6, height = buttonHeight, width = buttonWidth)
    factory = StringVar()
    #run query to fetch factories
    factory_values =[""] + getJsonValues('Factory')
    factoryEntry = OptionMenu(adSearchPage, factory, *factory_values)
    factoryEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*6, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Production Year').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*7, height = buttonHeight, width = buttonWidth)
    productionYear = StringVar()
    #run query to fetch productionYears
    productionYear_values =[""] + getJsonValues('ProductionYear')
    productionYearEntry = OptionMenu(adSearchPage, productionYear, *productionYear_values)
    productionYearEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*7, height = buttonHeight, width = buttonWidth)

    Label(adSearchPage, text = 'Power Supply').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*8, height = buttonHeight, width = buttonWidth)
    powerSupply = StringVar()
    #run query to fetch productionYears
    powerSupply_values =[""] + getJsonValues('PowerSupply')
    powerSupplyEntry = OptionMenu(adSearchPage, powerSupply, *powerSupply_values)
    powerSupplyEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*8, height = buttonHeight, width = buttonWidth)


    Label(adSearchPage, text = 'Item ID').place(x = (pageHeight/3*2 - 200), y = top_y + spacing*9, height = buttonHeight, width = buttonWidth)
    itemID = StringVar()
    #run query to fetch productionYears
    itemIDEntry = Entry(adSearchPage, textvariable = itemID)
    itemIDEntry.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*9, height = buttonHeight, width = buttonWidth)


    def executeSimpleSearch():
        global searchResult
        global checkSearch
        checkSearch = "Simple"
        categoryInput_S = category_S.get()
        modelInput_S = model_S.get()

        if categoryInput_S != "" and modelInput_S != "":
            category_S.set("")
            model_S.set("")
            return messagebox.showerror(title = 'Search Error',\
                                        message = 'Please key in EITHER Category or Model')
        elif categoryInput_S == "" and modelInput_S == "":
            return messagebox.showerror(title = 'Search Error',\
                                        message = 'No input: Please key in EITHER Category or Model')
        else:
            if categoryInput_S != "":
                searchResult = simpleSearchA(categoryInput_S)
            else:
                searchResult = simpleSearchA(modelInput_S)
        
        adSearchPageToAdResultPage()


    def executeAdvSearch():
        global searchResult
        global checkSearch
        checkSearch = "Advanced"
        categoryInput_A = category_A.get()
        modelInput_A = model_A.get()
        priceInput = price.get()
        warrantyInput = warranty.get()
        colourInput = colour.get()
        factoryInput = factory.get()
        productionYearInput = productionYear.get()
        powerSupplyInput = powerSupply.get()
        itemIDInput = itemIDEntry.get()
        
        global getItemID
        getItemID = itemIDInput        


        if warrantyInput != "":
            warrantyInput = int(warrantyInput)
        if priceInput != "":
            priceInput = int(priceInput)
            #print(len((priceInput, warrantyInput, categoryInput_A, modelInput_A, \
        #                         colourInput, factoryInput, productionYearInput, powerSupplyInput)))
        
        searchResult = advSearchA(priceInput, warrantyInput, itemIDInput, categoryInput_A, modelInput_A, \
                                  colourInput, factoryInput, productionYearInput, powerSupplyInput)

        if searchResult == []:
            messagebox.showerror(title = 'No Such Item',\
                                        message = 'No Such item available with the above filters')
        else:
            adSearchPageToAdResultPage()

        

    executeSimpleSearchButton = Button(adSearchPage, text = 'Simple Search', command = executeSimpleSearch,bg='peach puff')
    executeSimpleSearchButton.place(x = (pageHeight/3 - buttonWidth/2), y = top_y + spacing*10, height = buttonHeight, width = buttonWidth)

    executeAdvSearchButton = Button(adSearchPage, text = 'Advanced Search', command = executeAdvSearch,bg='peach puff')
    executeAdvSearchButton.place(x = (pageHeight/3*2 - buttonWidth/2), y = top_y + spacing*10, height = buttonHeight, width = buttonWidth)

    backToMainPageButton = Button(adSearchPage, text = 'Back to Main Page', command = adSearchPageToMainPage,bg='peach puff')
    backToMainPageButton.place(x = 1000, y = top_y + spacing*9, height = buttonHeight, width = buttonWidth)

 


## adResultPage ##
def adResultPageToAdSearchPage():
    adResultPage.destroy()
    adSearchPageFunction()


def adResultPageFunction():
    global adResultPage
    adResultPage = Toplevel()
    adResultPage.title('Admin Result Page')
    adResultPage.geometry(pageGeometry)
    my_label = Label(adResultPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    if checkSearch == "Simple":
        #load simple search results
        searchColumns = ('ProductID', 'Category', 'Model', 'Cost ($)', 'Price ($)', 'Warranty (months)', \
                                  'Inventory', 'Sold')
        searchTable = ttk.Treeview(adResultPage, columns= searchColumns, show='headings',\
                                   selectmode = "extended")
        
        searchTable.heading('ProductID', text = 'Product ID', anchor = CENTER)
        searchTable.column('ProductID', width = 120)
        searchTable.heading('Category', text = 'Category', anchor = CENTER)
        searchTable.column('Category', width = 120)
        searchTable.heading('Model', text = 'Model', anchor = CENTER)
        searchTable.heading('Cost ($)', text = 'Cost ($)', anchor = CENTER)
        searchTable.column('Cost ($)', width = 60)
        searchTable.heading('Price ($)', text = 'Price ($)', anchor = CENTER)
        searchTable.column('Price ($)', width = 60)
        searchTable.heading('Warranty (months)', text = 'Warranty (months)', anchor = CENTER)
        searchTable.column('Warranty (months)', width = 120)
        searchTable.heading('Inventory', text = 'Inventory', anchor = CENTER)
        searchTable.column('Inventory', width = 120)
        searchTable.heading('Sold', text = 'No. Products Sold', anchor = CENTER)
        searchTable.column('Sold', width = 120)

        #Center Values
        for column in searchColumns:
            searchTable.column(column, anchor = CENTER)

        for result in searchResult:
            resultTuple = ()
            for column in searchColumns:           
                resultTuple += (result[column],)
            searchTable.insert(parent = '', index = searchResult.index(result), values = resultTuple)
        searchTable.pack()

    else:
        #load advanced search results for when ItemID is keyed in 
        
        if getItemID != "":
            #if ItemID is not empty string, itemID index is 2 in searchResult
            
            searchColumns = ('ItemID', 'Category', 'Model','Cost ($)', 'Price ($)', 'Warranty (months)', \
                             'Color', 'Factory', 'ProductionYear', 'PowerSupply', 'PurchaseStatus')
            searchTable = ttk.Treeview(adResultPage, columns = searchColumns, show = 'headings')
            searchTable.heading('ItemID', text = 'Item ID', anchor = CENTER)
            searchTable.column('ItemID', width = 60)
            searchTable.heading('Category', text = 'Category', anchor = CENTER)
            searchTable.column('Category', width = 120)
            searchTable.heading('Model', text = 'Model', anchor = CENTER)
            searchTable.heading('Cost ($)', text = 'Cost ($)', anchor = CENTER)
            searchTable.column('Cost ($)', width = 60)
            searchTable.heading('Price ($)', text = 'Price ($)', anchor = CENTER)
            searchTable.column('Price ($)', width = 60)
            searchTable.heading('Warranty (months)', text = 'Warranty (months)', anchor = CENTER)
            searchTable.column('Warranty (months)', width = 120)
            searchTable.heading('Color', text = 'Color', anchor = CENTER)
            searchTable.column('Color', width = 120)
            searchTable.heading('Factory', text = 'Factory', anchor = CENTER)
            searchTable.column('Factory', width = 120)
            searchTable.heading('ProductionYear', text = 'Production Year', anchor = CENTER)
            searchTable.column('ProductionYear', width = 120)
            searchTable.heading('PowerSupply', text = 'Power Supply', anchor = CENTER)
            searchTable.column('PowerSupply', width = 120)
            searchTable.heading('PurchaseStatus', text = 'Purchase Status', anchor = CENTER)
            searchTable.column('PurchaseStatus', width = 120)
        

            #Center Values
            for column in searchColumns:
                searchTable.column(column, anchor = CENTER)
            resultTuple = ()
            if searchResult != []:
                for column in searchColumns:
                    resultTuple += (searchResult[0][column],)
                searchTable.insert(parent = '', index = 0, values = resultTuple)
                

        else:
            #ItemID is not entered
            searchColumns = ('Category', 'Model','Cost ($)', 'Price ($)', 'Warranty (months)', \
                             'Color', 'Factory', 'ProductionYear', 'PowerSupply', 'Inventory',\
                             'Sold')
            searchTable = ttk.Treeview(adResultPage, columns = searchColumns, show = 'headings')
            searchTable.heading('Category', text = 'Category', anchor = CENTER)
            searchTable.column('Category', width = 120)
            searchTable.heading('Model', text = 'Model', anchor = CENTER)
            searchTable.heading('Cost ($)', text = 'Cost ($)', anchor = CENTER)
            searchTable.column('Cost ($)', width = 60)
            searchTable.heading('Price ($)', text = 'Price ($)', anchor = CENTER)
            searchTable.column('Price ($)', width = 60)
            searchTable.heading('Warranty (months)', text = 'Warranty (months)', anchor = CENTER)
            searchTable.column('Warranty (months)', width = 120)
            searchTable.heading('Color', text = 'Color', anchor = CENTER)
            searchTable.column('Color', width = 120)
            searchTable.heading('Factory', text = 'Factory', anchor = CENTER)
            searchTable.column('Factory', width = 120)
            searchTable.heading('ProductionYear', text = 'Production Year', anchor = CENTER)
            searchTable.column('ProductionYear', width = 120)
            searchTable.heading('PowerSupply', text = 'Power Supply', anchor = CENTER)
            searchTable.column('PowerSupply', width = 120)
            searchTable.heading('Inventory', text = 'Inventory', anchor = CENTER)
            searchTable.column('Inventory', width = 120)
            searchTable.heading('Sold', text = 'No. of Items Sold', anchor = CENTER)

            

            #Center Values
            for column in searchColumns:
                searchTable.column(column, anchor = CENTER)


            finalResult ={}
            for result in searchResult:
                resultTuple = ()

                for column in searchColumns[:-2]:
                    resultTuple += (result[column],)
       
                if resultTuple not in finalResult:
                    if result["PurchaseStatus"] == 'Unsold':
                        finalResult[resultTuple] = [1,0]
                    else:
                        finalResult[resultTuple] = [0,1]
                else:
                    if result["PurchaseStatus"] == 'Unsold':
                        finalResult[resultTuple][0] += 1
                    else:
                        finalResult[resultTuple][1] += 1
            finalList = []
            for k, v in finalResult.items():
                finalList.append(k + (v[0],v[1]))
            for entry in finalList:
                searchTable.insert(parent='', index = finalList.index(entry), values = entry)

            #ItemID is empty string







    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")
    searchTable.pack()
    
    


    xscrollbar = ttk.Scrollbar(adResultPage, orient="horizontal", command=searchTable.xview)
    xscrollbar.pack(side="bottom", fill="x")
    

    newSearchButton = Button(adResultPage, text='New Search', command=adResultPageToAdSearchPage,bg='peach puff')
    newSearchButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=650, height=buttonHeight, width=buttonWidth)


## reqPage ##
def reqPageToMainPage():
    reqPage.destroy()
    mainPageFunction()

def refreshReqPage():
    reqPage.destroy()
    reqPageFunction()


def reqPageFunction():
    global reqPage
    reqPage = Toplevel()
    reqPage.title('Request Management Page')
    reqPage.geometry(pageGeometry)
    my_label = Label(reqPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    result_columns = ('#1', '#2', '#3', '#4', '#5', '#6')
    result_table = ttk.Treeview(reqPage, columns=result_columns, show='headings')
    result_table.heading('#1', text='RequestID')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='ItemID')
    result_table.column('#2', width = 60)
    result_table.heading('#3', text='CustomerID')
    result_table.column('#3', width = 120)
    result_table.heading('#4', text='Submission Date')
    result_table.column('#4', width = 120)
    result_table.heading('#5', text='Request Status')
    result_table.heading('#6', text='AdminID')
    result_table.column('#6', width = 120)
    result_table.pack()

    for column in result_columns:
        result_table.column(column, anchor = CENTER)
        
    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")
    result_table.pack()

    xscrollbar = ttk.Scrollbar(reqPage, orient="horizontal", command=result_table.xview)
    xscrollbar.pack(side="bottom", fill="x")

    unpaid_table = read_query(connection, "SELECT * FROM servicerequests "
                              "WHERE RequestStatus IN ('Submitted', 'In Progress') "
                              "GROUP BY RequestID;")

    for i in range(len(unpaid_table)):
        result_table.insert(parent='', index=i,
                            values=(unpaid_table[i][0], unpaid_table[i][1], unpaid_table[i][2], unpaid_table[i][3],
                                    unpaid_table[i][4], unpaid_table[i][5]))

    def approveRequest():
        try:
            row = result_table.selection()
            
            if len(row) == 0:
                return messagebox.showerror(title='Error', message='Please Select a Reqeust to Approve')
            
            for i in row:
                reqID = result_table.item(i)['values'][0]
                itemID = result_table.item(i)['values'][1]
                execute_query(connection, "UPDATE servicerequests SET requeststatus='Approved' , adminid='%s' WHERE requestid='%s'" % (CurrentUserID, reqID))
                execute_query(connection, "UPDATE items SET servicestatus='In Progress' WHERE itemid='%s'" % (itemID))
            refreshReqPage()
            return messagebox.showinfo(title = 'Success', message = 'Request successfully approved!')
        except Exception as e:
            print(e)
            return messagebox.showerror(title = 'Error', message = 'Unable to approve request!')
        

    approveRequestButton = Button(reqPage, text='Approve', command=approveRequest,bg='peach puff')
    approveRequestButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)

    
    backToMainPageButton = Button(reqPage, text='Back to Main Page', command=reqPageToMainPage,bg='peach puff')
    backToMainPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=650, height=buttonHeight, width=buttonWidth)

    

## servicePage ##
def servicePageToMainPage():
    servicePage.destroy()
    mainPageFunction()

def refreshServicePage():
    servicePage.destroy()
    servicePageFunction()

def servicePageFunction():
    global servicePage
    servicePage = Toplevel()
    servicePage.title('Service Management Page')
    servicePage.geometry(pageGeometry)
    my_label = Label(servicePage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    result_columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
    result_table = ttk.Treeview(servicePage, columns=result_columns, show='headings')
    result_table.heading('#1', text='RequestID')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='ItemID')
    result_table.column('#2', width = 60)
    result_table.heading('#3', text='CustomerID')
    result_table.column('#3', width = 120)
    result_table.heading('#4', text='Submission Date')
    result_table.column('#4', width = 120)
    result_table.heading('#5', text='Request Status')
    result_table.heading('#6', text='AdminID')
    result_table.column('6', width = 120)
    result_table.heading('#7', text='Service Status')
    result_table.pack()

    xscrollbar = ttk.Scrollbar(servicePage, orient="horizontal", command=result_table.xview)
    xscrollbar.pack(side="bottom", fill="x")

    service_table = read_query(connection, "SELECT S.RequestID, S.ItemID, S.CustomerID, "
                               "S.SubmissionDate, S.RequestStatus, S.AdminID, I.ServiceStatus "
                               "FROM servicerequests S JOIN items I ON "
                               "I.ItemID = S.ItemID "
                               "WHERE AdminID='%s' "
                               "AND S.RequestStatus='Approved' AND I.ServiceStatus='In Progress' "
                               "GROUP BY RequestID;" % (CurrentUserID))


    for column in result_columns:
        result_table.column(column, anchor = CENTER)

    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")
    result_table.pack()

    for i in range(len(service_table)):
        result_table.insert(parent='', index=i,
                            values=(service_table[i][0], service_table[i][1], service_table[i][2], service_table[i][3],
                                    service_table[i][4], service_table[i][5], service_table[i][6]))

    def completeService():
        try:
            row = result_table.selection()
            
            if len(row) == 0:
                return messagebox.showerror(title='Error', message='Please Select an Item to Service')
            for i in row:
                reqID = result_table.item(i)['values'][0]
                itemID = result_table.item(i)['values'][1]
                execute_query(connection, "UPDATE servicerequests SET requeststatus='Completed' WHERE requestid='%s'" % (reqID))
                execute_query(connection, "UPDATE items SET servicestatus='Completed' WHERE itemid='%s'" % (itemID))
            refreshServicePage()
            return messagebox.showinfo(title = 'Success', message = 'Item servicing completed!')
        except Exception as e:
            print(e)
            return messagebox.showerror(title = 'Error', message = 'Unable to complete servicing!')

        

    completeServiceButton = Button(servicePage, text='Finish Servicing', command=completeService,bg='peach puff')
    completeServiceButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)

    

    backToMainPageButton = Button(servicePage, text='Back to Main Page', command=servicePageToMainPage,bg='peach puff')
    backToMainPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=650, height=buttonHeight, width=buttonWidth)


## adFuncPage ##
def adFuncPageToMainPage():
    adFuncPage.destroy()
    mainPageFunction()


def adFuncPageToItemsSoldPage():
    adFuncPage.destroy()
    itemsSoldPageFunction()


def adFuncPageToItemServicePage():
    adFuncPage.destroy()
    itemServicePageFunction()


def adFuncPageToCustomerUnpaidPage():
    adFuncPage.destroy()
    customerUnpaidPageFunction()


def adFuncPageToMySqlInitPage():
    adFuncPage.destroy()
    mySqlInitPageFunction()


def adFuncPageFunction():
    global adFuncPage
    adFuncPage = Toplevel()
    adFuncPage.title('Administrator Functions Page')
    adFuncPage.geometry(pageGeometry)
    my_label = Label(adFuncPage, image=pink)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    Label(adFuncPage,image=oshes2).place(x = (pageHeight/2 - 190), y = 0, height = 100, width = 360)

    def itemSold():
        adFuncPageToItemsSoldPage()
        # return items sold
        
    itemSoldButton = Button(adFuncPage, text='View Items Sold', command=itemSold,bg='peach puff')
    itemSoldButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=250, height=buttonHeight, width=buttonWidth)

    def itemService():
        adFuncPageToItemServicePage()
        # return items under servicing

    itemUnderServiceButton = Button(adFuncPage, text='View Items Under Service', command=itemService,bg='peach puff')
    itemUnderServiceButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=350, height=buttonHeight, width=buttonWidth)

    def customerUnpaid():
        adFuncPageToCustomerUnpaidPage()
        # return customers with unpaid service requests

    customerUnpaidButton = Button(adFuncPage, text='Unpaid Service Requests', command=customerUnpaid,bg='peach puff')
    customerUnpaidButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=450, height=buttonHeight, width=buttonWidth)

    def mySqlInit():
        global connection
        connection = re_init(connection)
        time.sleep(5)
        adFuncPageToMySqlInitPage()

    mySqlInitButton = Button(adFuncPage, text='mySQL Initialisation', command=mySqlInit,bg='peach puff')
    mySqlInitButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)

    backToMainPageButton = Button(adFuncPage, text='Back to Main Page', command=adFuncPageToMainPage,bg='peach puff')
    backToMainPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=650, height=buttonHeight, width=buttonWidth)


## itemsSoldPage ##
def itemsSoldPageToAdFuncPage():
    itemsSoldPage.destroy()
    adFuncPageFunction()


def itemsSoldPageFunction():
    global itemsSoldPage
    itemsSoldPage = Toplevel()
    itemsSoldPage.title('Items Sold Page')
    itemsSoldPage.geometry(pageGeometry)
    my_label = Label(itemsSoldPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    result_columns = ('#1', '#2', '#3')
    result_table = ttk.Treeview(itemsSoldPage, columns=result_columns, show='headings')
    result_table.heading('#1', text='Category')
    result_table.column('#1', width = 120)
    result_table.heading('#2', text='Model')
    result_table.heading('#3', text='Number of Sold Items')
    result_table.pack()


    for column in result_columns:
        result_table.column(column, anchor = CENTER)
        
    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")


    items_sold_table = read_query(connection, "SELECT P.Category, P.Model, "
                                              "SUM(case when I.PurchaseStatus = 'Sold' then 1 else 0 end) SoldItems "
                                              "FROM products P JOIN items I ON "
                                              "I.Category = P.Category AND I.Model = P.Model "
                                              "GROUP BY P.ProductID;")
    for i in range(len(items_sold_table)):
        result_table.insert(parent='', index=i,
                            values=(items_sold_table[i][0], items_sold_table[i][1], int(items_sold_table[i][2])))

    backToAdFuncPageButton = Button(itemsSoldPage, text='Back', command=itemsSoldPageToAdFuncPage,bg='peach puff')
    backToAdFuncPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)


## itemServicePage ##
def itemServicePageToAdFuncPage():
    itemServicePage.destroy()
    adFuncPageFunction()


def itemServicePageFunction():
    global itemServicePage
    itemServicePage = Toplevel()
    itemServicePage.title('Items Under Servicing')
    itemServicePage.geometry(pageGeometry)
    my_label = Label(itemServicePage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    result_columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7')
    result_table = ttk.Treeview(itemServicePage, columns=result_columns, show='headings')
    result_table.heading('#1', text='ItemID')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='RequestID')
    result_table.column('#2', width = 60)
    result_table.heading('#3', text='CustomerID')
    result_table.column('#3', width = 120)
    result_table.heading('#4', text='Submission Date')
    result_table.column('#4', width = 120)
    result_table.heading('#5', text='Request Status')
    result_table.heading('#6', text='AdminID')
    result_table.column('#6', width = 120)
    result_table.heading('#7', text='Service Status')
    result_table.pack()

    for column in result_columns:
        result_table.column(column, anchor = CENTER)

    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")


    xscrollbar = ttk.Scrollbar(itemServicePage, orient="horizontal", command=result_table.xview)
    xscrollbar.pack(side="bottom", fill="x")

    
    service_table = read_query(connection, "SELECT ItemID, ServiceStatus "
                               "FROM items "
                               "WHERE ServiceStatus in ('Waiting for Approval', 'In Progress') "
                               "GROUP BY ItemID; ")

    items_id_table = []
    for entry in service_table:
        items_id_table.append(entry[0])

    request_status_table = []
    for i in items_id_table:
        next_status = read_query(connection, "SELECT requestid, requeststatus, submissiondate, customerid, adminid FROM servicerequests WHERE itemid='%s';" % (i))
        if len(next_status) == 0:
            request_status_table.append(['','','','',''])
        else:
            request_status_table.append(next_status[-1])

    for i in range(len(service_table)):
        result_table.insert(parent='', index=i,
                            values=(service_table[i][0], request_status_table[i][0], request_status_table[i][3], request_status_table[i][2],
                                    request_status_table[i][1], request_status_table[i][4], service_table[i][1]))

    backToAdFuncPageButton = Button(itemServicePage, text='Back', command=itemServicePageToAdFuncPage,bg='peach puff')
    backToAdFuncPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)


## customerUnpaidPage ##
def customerUnpaidPageToAdFuncPage():
    customerUnpaidPage.destroy()
    adFuncPageFunction()


def customerUnpaidPageFunction():
    global customerUnpaidPage
    customerUnpaidPage = Toplevel()
    customerUnpaidPage.title('Customers With Unpaid Service Requests Page')
    customerUnpaidPage.geometry(pageGeometry)
    my_label = Label(customerUnpaidPage, image=rainbow)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    result_columns = ('#1', '#2', '#3', '#4', '#5', '#6')
    result_table = ttk.Treeview(customerUnpaidPage, columns=result_columns, show='headings')
    result_table.heading('#1', text='RequestID')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='ItemID')
    result_table.column('#2', width = 60)
    result_table.heading('#3', text='CustomerID')
    result_table.column('#3', width = 120)
    result_table.heading('#4', text='Submission Date')
    result_table.column('#4', width = 120)
    result_table.heading('#5', text='Request Status')
    result_table.heading('#6', text='AdminID')
    result_table.column('#6', width = 60)
    result_table.pack()
    
    for column in result_columns:
        result_table.column(column, anchor = CENTER)

    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")

    xscrollbar = ttk.Scrollbar(customerUnpaidPage, orient="horizontal", command=result_table.xview)
    xscrollbar.pack(side="bottom", fill="x")

    unpaid_table = read_query(connection, "SELECT * FROM servicerequests "
                                          "WHERE RequestStatus='Submitted and Waiting for Payment' "
                                          "GROUP BY RequestID;")

    for i in range(len(unpaid_table)):
        result_table.insert(parent='', index=i,
                            values=(unpaid_table[i][0], unpaid_table[i][1], unpaid_table[i][2], unpaid_table[i][3],
                                    unpaid_table[i][4], unpaid_table[i][5]))

    backToAdFuncPageButton = Button(customerUnpaidPage, text='Back', command=customerUnpaidPageToAdFuncPage,bg='peach puff')
    backToAdFuncPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)
    

## mySqlInitPage ##
def mySqlInitPageToAdFuncPage():
    mySqlInitPage.destroy()
    adFuncPageFunction()

def mySqlInitPageFunction():
    global mySqlInitPage
    mySqlInitPage = Toplevel()
    mySqlInitPage.title('mySQL Initialisation Results Page')
    mySqlInitPage.geometry(pageGeometry)
    my_label = Label(mySqlInitPage, image=pink)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)
    Label(mySqlInitPage,image=oshes2).place(x = (pageHeight/2 - 190), y = 0, height = 100, width = 360)

    result_columns = ('#1', '#2', '#3')
    result_table = ttk.Treeview(mySqlInitPage, columns=result_columns, show='headings')
    result_table.heading('#1', text='IID')
    result_table.column('#1', width = 60)
    result_table.heading('#2', text='Number of Sold Items')
    result_table.heading('#3', text='Number of Unsold Items')

    result_table.pack()


    for column in result_columns:
        result_table.column(column, anchor = CENTER)

    style = ttk.Style()
    style.theme_use('default')
    style.map("Treeview")

    
    product_table = read_query(connection, "SELECT P.ProductID, "
                                           "SUM(case when I.PurchaseStatus = 'Sold' then 1 else 0 end) SoldItems, "
                                           "SUM(case when I.PurchaseStatus = 'Unsold' then 1 else 0 end) UnsoldItems "
                                           "FROM products P JOIN items I ON "
                                           "I.Category = P.Category AND I.Model = P.Model "
                                           "GROUP BY P.ProductID;")
    for i in range(len(product_table)):
        result_table.insert(parent='', index=i,
                            values=(product_table[i][0], int(product_table[i][1]), int(product_table[i][2])))

    backToAdFuncPageButton = Button(mySqlInitPage, text='Back', command=mySqlInitPageToAdFuncPage,bg='peach puff')
    backToAdFuncPageButton.place(x=(pageHeight / 2 - buttonWidth / 2), y=550, height=buttonHeight, width=buttonWidth)

    #Restart mongo database
    reinitializeMongo()



## root ##
root = Tk()


def openMain():
    loginPageFunction()
    checkallreq="SELECT requestID,Submissiondate,itemID FROM servicerequests WHERE requeststatus='Submitted and Waiting for Payment'"
    pendingreq=read_query(connection,checkallreq)
    if len(pendingreq)==0:
        return None
    else:
        for req in pendingreq:
            date_time_obj = datetime. strptime(str(req[1]),'%Y-%m-%d')
            newdate=date_time_obj+relativedelta(days=+10)

            today=datetime.strptime(date_input,'%Y-%m-%d')
            if today>newdate:
                cancelupdate="UPDATE items SET servicestatus='' WHERE itemID='%s'"%(req[2])
                execute_query(connection,cancelupdate)
                execute_query(connection,"Update servicerequests SET requeststatus='Cancelled' WHERE requestID='%s'"%(req[0]))
                execute_query(connection,"DELETE FROM servicefee WHere requestID='%s'"%(req[0]))
                
            else:
                continue

###Add pictures###
root.title('Home Page')
root.iconbitmap(r'C:\Users\raych\Downloads\GRP_17_AS1')
root.geometry("600x300")
pink=PhotoImage(file=r'C:\Users\raych\Downloads\GRP_17_AS1\mainscreen.png')
rainbow=PhotoImage(file=r'C:\Users\raych\Downloads\GRP_17_AS1\mainscreen.png')
oshes=PhotoImage(file=r'C:\Users\raych\Downloads\GRP_17_AS1\start.png')
oshes2=PhotoImage(file=r'C:\Users\raych\Downloads\GRP_17_AS1\picture10.png')
my_label = Label(root, image = oshes)
my_label.place(x=0,y=0,relwidth=1,relheight=1)


Label(root, text = 'Welcome to OSHES, Press Start to Begin',bg='black', fg = 'white', font='Verdana 12 bold').place(x = 100, y = 20, height = 20, width = 400)


startButton = Button(root, text='Start', command=openMain, height=5, width=20,bg='SteelBlue1',font='Verdana 9 bold').place(x=220,y=100)
root.mainloop()
#adding pic to button
