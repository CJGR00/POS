import mysql.connector
from mysql.connector import Error

# Database connection details
host = 'localhost'
user = 'root'                   # Replace with your MySQL username
password = '#@01001ej47bloom'   # Replace with your MySQL password
database_name = 'pyhorsedb'

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS inventory (
            ProductID INT AUTO_INCREMENT PRIMARY KEY, 
            ProductName VARCHAR(255) NOT NULL, 
            Category VARCHAR(255), 
            Price INT,       
            Stock INT, 
            DateAdded DATE)''')
    connection.commit()
    connection.close()

def fetch_products():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM inventory")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def name_exist(name):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventory WHERE ProductName = %s", (name,))
    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return result > 0


def insert_product(name, category, stock, price, date):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO inventory (ProductName, Category, Price, Stock, DateAdded) VALUES (%s, %s, %s, %s, %s)", (name, category, price, stock, date))
    connection.commit()
    connection.close()
    return

def update_product(new_name, new_category, new_price, new_stock, new_date, id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE inventory SET ProductName = %s, Category = %s, Price= %s, Stock = %s, DateAdded = %s WHERE ProductID = %s", (new_name, new_category, new_price, new_stock, new_date, id))
    connection.commit()
    connection.close()



def delete_product(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM inventory WHERE ProductID = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()     

create_table()                