# file: persistence.py
import atexit
import sqlite3
import os


# import atexit


# Data Transfer Objects:
class Employees(object):
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand


class Suppliers(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information


class Products(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity


class Coffee_stands(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees


class Activities(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date


# Data Access Objects:
# All of these are meant to be singletons
class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO Employees (id, name, salary,coffee_stand) VALUES (?, ?, ?, ?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def get_table(self):
        c = self._conn.cursor()
        return c.execute("""
        SELECT id, name, salary,coffee_stand FROM Employees ORDER BY id ASC
        """).fetchall()


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, suppliers):
        self._conn.execute("""
                INSERT INTO Suppliers (id, name, contact_information) VALUES (?, ?, ?)
        """, [suppliers.id, suppliers.name, suppliers.contact_information])

    def get_table(self):
        c = self._conn.cursor()
        return c.execute('SELECT * FROM Suppliers ORDER BY id ASC').fetchall()


class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
            INSERT INTO Products (id, description, price, quantity) VALUES (?, ?, ?, ?)
        """, [product.id, product.description, product.price, product.quantity])

    def get_table(self):
        c = self._conn.cursor()
        return c.execute('SELECT * FROM Products ORDER BY id ASC').fetchall()

    def get_product(self, product_id):
        c = self._conn.cursor()
        return Products(*(c.execute("""SELECT * FROM Products WHERE id = ?""", [product_id]).fetchone()))

    def update_quantity(self, product_id, product_quantity):
        c = self._conn.cursor()
        c.execute("""
        UPDATE Products SET quantity = ? WHERE id = ?
        """, [product_quantity, product_id])


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
        INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
        """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def get_table(self):
        c = self._conn.cursor()
        return c.execute('SELECT * FROM Coffee_stands ORDER BY id ASC').fetchall()


class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activities):
        self._conn.execute("""
            INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
        """, [activities.product_id, activities.quantity, activities.activator_id, activities.date])

    def get_table(self):
        c = self._conn.cursor()
        return c.execute('SELECT * FROM Activities ORDER BY date ASC').fetchall()

    def add_activity(self, activity):
        c = self._conn.cursor()
        c.execute('INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)',
                  [activity.product_id, activity.quantity, activity.activator_id, activity.date])

        # For join query


class EmployeeReport(object):
    def __init__(self, name, salary, location, sales):
        self.name = name
        self.salary = salary
        self.location = location
        self.sales = sales


# The Repository
class Repository:
    def __init__(self):
        # self.dbExist = os.path.isfile('moncafe.db')
        self._conn = sqlite3.connect('moncafe.db')
        self._conn.text_factory = str
        self.employees = _Employees(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.products = _Products(self._conn)
        self.coffee_stands = _Coffee_stands(self._conn)
        self.activities = _Activities(self._conn)

    # if self.dbExist: #todo: check if needed
    #	os.remove('moncafe.db')

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def get_employees_report(self):
        c = self._conn.cursor()
        report = c.execute("""SELECT Employees.name, Employees.salary, Coffee_stands.location, 
                             COALESCE (SUM(Activities.quantity * Products.price * (-1)),0)
                             FROM (Employees INNER JOIN Coffee_stands ON Employees.coffee_stand = Coffee_stands.id
                             LEFT OUTER JOIN Activities ON Employees.id = Activities.activator_id
                             LEFT OUTER JOIN products ON Activities.product_id = Products.id )
                             GROUP BY Employees.id ORDER BY Employees.name""").fetchall()
        return [EmployeeReport(*row) for row in report]

    def get_activity_report(self):
        c = self._conn.cursor()
        return c.execute("""SELECT Activities.date, Products.description, Activities.quantity,
         Employees.name ,
         Suppliers.name
              FROM Activities
              LEFT JOIN Products ON Activities.product_id = Products.id
              LEFT JOIN Employees ON Activities.activator_id = Employees.id  
              LEFT JOIN Suppliers ON Activities.activator_id = Suppliers.id
            ORDER BY Activities.date ASC""").fetchall()

    def create_tables(self):
        self._conn.executescript("""
                    CREATE TABLE Suppliers (
                        id                          INTEGER     PRIMARY KEY,
                        name                        TEXT        NOT NULL,
                        contact_information         TEXT
                    );
    
                    CREATE TABLE Products (
                        id              INTEGER     PRIMARY KEY,
                        description     TEXT        NOT NULL,
                        price           REAL        NOT NULL,
                        quantity        INTEGER     NOT NULL
    
                    );
                    
                    CREATE TABLE Coffee_stands (
                        id              INTEGER     PRIMARY KEY,
                        location        TEXT        NOT NULL,
                        number_of_employees         INTEGER
                    );
                    
                    CREATE TABLE Employees (
                        id                              INTEGER     PRIMARY KEY,
                        name                            TEXT        NOT NULL,
                        salary                          REAL        NOT NULL,
                        coffee_stand                    INTEGER     REFERENCES Coffee_stands(id)
                    );
                    
                    CREATE TABLE Activities (
                        product_id          INTEGER     REFERENCES Products(id), 
                        quantity            INTEGER     NOT NULL,
                        activator_id        INTEGER     NOT NULL,
                        date                DATE        NOT NULL 
                    );
                """)


# we change, here some check!!!!
# see code in previous version...

# the repository singleton
repo = Repository()
atexit.register(repo._close)
