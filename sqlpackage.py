import mysql.connector
import json


# initial function to connect with mySQL
def establish_connection(hostname, username, pw):
    # global variables to store mySQL login
    global host_name
    global user_name
    global password

    host_name = hostname
    user_name = username
    password = pw

    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=password,
        )
        print("Connection to mySQL established")

        # creating oshes database
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS oshes;")
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=password,
            database="oshes"
        )
        print("Connected to oshes")
        connection.autocommit = False

    except Exception as e:
        print(e)
        print("Unable to connect to mySQL, please check your mySQL login details")

    return connection


# helper function to ensure connection is maintained
def reconnect():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=password,
            database="oshes"
        )
        print("Successfully reconnected to mySQL")
    except Exception as e:
        print(e)
        print("Unable to reconnect to mySQL")
    return connection


# function to reinitialise mySQL database
def re_init(connection):
    try:
        cursor = connection.cursor()
        # drop tables in reverse order
        cursor.execute("DROP TABLE IF EXISTS ServiceFee;")
        cursor.execute("DROP TABLE IF EXISTS ServiceRequests;")
        cursor.execute("DROP TABLE IF EXISTS Items;")
        cursor.execute("DROP TABLE IF EXISTS Customers;")
        cursor.execute("DROP TABLE IF EXISTS Products;")
        connection = reconnect()
        connection.autocommit = True
        connection = tables_init(connection)
        print("Successfully reinitialised all tables except Admins")
    except Exception as e:
        print(e)
        print("Unable to reinitialise tables")
    return connection


# function to upload json files onto mySQL and create all tables in database
def tables_init(connection):
    raw_products = open('products.json')
    raw_items = open('items.json')
    products = json.load(raw_products)
    items = json.load(raw_items)

    # constructing queries to insert json files

    products_query = ""
    for entry in products:
        next_entry = ""
        for value in entry.values():
            next_value = ""
            if type(value) == str:
                next_value = ", '" + value + "'"
            else:
                next_value = ", " + str(value) + " "
            next_entry += next_value
        next_entry = next_entry[2:]
        next_query = "INSERT INTO products VALUES ( %s );" % next_entry
        products_query += next_query

    items_query = ""
    for entry in items:
        next_entry = ""
        for value in entry.values():
            next_value = ""
            if type(value) == str:
                next_value = ", '" + value + "'"
            else:
                next_value = ", " + str(value) + " "
            next_entry += next_value
        # adds two NULL entries for our created attributes, CustomerID and purchaseDate
        next_entry = next_entry[2:] + ", NULL, NULL"
        next_query = "INSERT INTO items VALUES ( %s );" % next_entry
        items_query += next_query

    # create products table
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Products("
                   "Category VARCHAR(6) CONSTRAINT ProductCategory CHECK(Category IN ('Lights', 'Locks')) NOT NULL, "
                   "Cost INT NOT NULL, "
                   "Model VARCHAR(10) CONSTRAINT ProductModel CHECK(Model IN ('Light1', 'Light2','SmartHome1','Safe1','Safe2','Safe3')) NOT NULL, "
                   "Price INT NOT NULL, "
                   "ProductID INT NOT NULL, "
                   "Warranty INT NOT NULL, "
                   "PRIMARY KEY (Category,Model)"
                   ");")

    # inserts json file if currently empty
    if len(read_query(connection, "SELECT * FROM Products;")) == 0:
        cursor.execute(products_query)

    # create customers table
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Customers("
                   "CustomerID VARCHAR(50) NOT NULL, "
                   "Name VARCHAR(50) NOT NULL, "
                   "Gender VARCHAR(7) CONSTRAINT CustomerGender CHECK(Gender IN ('Male', 'Female')), "
                   "Email VARCHAR(50) NOT NULL, "
                   "Phone INT NOT NULL, "
                   "Address VARCHAR(50) NOT NULL, "
                   "Password VARCHAR(50) NOT NULL, "
                   "PRIMARY KEY (CustomerID) "
                   ");")

    # create items table
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Items("
                   "ItemID VARCHAR(5) NOT NULL, "
                   "Category VARCHAR(6) CONSTRAINT ItemCategory CHECK(Category IN ('Lights', 'Locks')) NOT NULL, "
                   "Color VARCHAR(10) NOT NULL, "
                   "Factory VARCHAR(15) NOT NULL, "
                   "PowerSupply VARCHAR(15) NOT NULL, "
                   "PurchaseStatus VARCHAR(6) CONSTRAINT Purchase CHECK(PurchaseStatus IN ('Sold', 'Unsold')) NOT NULL, "
                   "ProductionYear VARCHAR(4) NOT NULL, "
                   "Model VARCHAR(10) CONSTRAINT ItemModel CHECK(Model IN ('Light1', 'Light2','SmartHome1','Safe1','Safe2','Safe3')) NOT NULL, "
                   "ServiceStatus VARCHAR(100), "
                   "CustomerID VARCHAR(50), "
                   "PurchaseDate DATE, "
                   "PRIMARY KEY (ItemID), "
                   "FOREIGN KEY (Category, Model) REFERENCES Products (Category,Model), "
                   "FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)"
                   ");")

    # inserts json file if currently empty
    if len(read_query(connection, "SELECT * FROM Items;")) == 0:
        cursor.execute(items_query)

    # create admin table
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Admins("
                   "AdminID VARCHAR(50) NOT NULL, "
                   "Name VARCHAR(50) NOT NULL, "
                   "Gender VARCHAR(7) CONSTRAINT AdminGender CHECK(Gender IN ('Male', 'Female')), "
                   "Phone INT NOT NULL, "
                   "Password VARCHAR(50) NOT NULL, "
                   "PRIMARY KEY (AdminID) "
                   ");")

    # create serviceRequests table
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ServiceRequests("
                   "RequestID INT NOT NULL AUTO_INCREMENT, "
                   "ItemID VARCHAR(5) NOT NULL, "
                   "CustomerID VARCHAR(50) NOT NULL, "
                   "SubmissionDate DATE NOT NULL, "
                   "RequestStatus VARCHAR(100) NOT NULL, "
                   "AdminID VARCHAR(50), "
                   "PRIMARY KEY (RequestID), "
                   "FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID), "
                   "FOREIGN KEY (AdminID) REFERENCES Admins (AdminID) "
                   ");")
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE ServiceRequests AUTO_INCREMENT=1000;")

    # create serviceFee table
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ServiceFee("
                   "RequestID INT NOT NULL AUTO_INCREMENT, "
                   "Fee DOUBLE NOT NULL, "
                   "CustomerID VARCHAR(50) NOT NULL, "
                   "PaymentDate DATE, "
                   "PRIMARY KEY (RequestID), "
                   "FOREIGN KEY (RequestID) REFERENCES ServiceRequests (RequestID), "
                   "FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID) "
                   ");")
    connection = reconnect()
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("ALTER TABLE ServiceFee AUTO_INCREMENT=1000;")

    connection = reconnect()

    return connection


# function to execute read-only queries
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print("Successfully fetched information from query")
    except Exception as e:
        print(e)
        print("Unable to run read query")
    return result


# function to execute SINGULAR queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Successfully executed query")
    except Exception as e:
        print(e)
        print("Unable to execute query")
