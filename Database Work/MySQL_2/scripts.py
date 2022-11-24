from mysql import connector
import variables
from random import randint


def create_database(my_cursor ,name:str):
    """Create MySQL schema (database)
    
    my_curser: CMySQLCursor
    name: alias for MySQL schema(database)
    """
    my_cursor.execute(f"""CREATE DATABASE {name}""")
    my_cursor.execute(f"""use {name}""")

    print(f"Using db:{name}")

def create_tables(my_cursor):

    """This code creates tables necesary for the "banking" database we intend to use.
    
    my_curser: CMySQLCursor"""
    
    my_cursor.execute("""
    CREATE TABLE Suppliers (
        sid INT AUTO_INCREMENT, 
        sname VARCHAR(63),
        city VARCHAR(63),
        street VARCHAR(127),
        PRIMARY KEY(sid)) 
        
        ENGINE=InnoDB
    """)

    my_cursor.execute("""
    CREATE TABLE Parts (
        sku INT AUTO_INCREMENT,
        pname VARCHAR(31), 
        stock_level INT, 
        color VARCHAR(63), 
        PRIMARY KEY(sku)) 
        
        ENGINE=InnoDB
    """)

    my_cursor.execute("""
    CREATE TABLE Catalog (
        sid INT, 
        sku INT, 
        unit_price FLOAT, 
        FOREIGN KEY (sid) REFERENCES Suppliers(sid), 
        FOREIGN KEY (sku) REFERENCES Parts(sku))
        
        ENGINE=InnoDB    
    """)

    my_cursor.execute("""
    CREATE TABLE Orders (
        oid INT AUTO_INCREMENT, 
        sid INT, 
        sku INT, 
        quantity INT, 
        PRIMARY KEY (oid), 
        FOREIGN KEY (sid) REFERENCES Suppliers(sid), 
        FOREIGN KEY (sku) REFERENCES Parts(sku))

        ENGINE=InnoDB
    """)

    print("Tables created")

def sample_imput(my_cursor, size: int):
    c_size = len(variables.i_colour)
    n_size = len(variables.i_name)
    s_size = len(variables.s_data)
    
    catalog = {}
    order_data = []
    parts = {}

    #Sample Imput
    for x in range(size):
        price = float(randint(1,100))/(100.0)
        #Price range 0-1
        quantity = randint(1,5)
        #Quantity range per order is 1-5


        supplier = variables.s_data[randint(0,s_size-1)]
        sid = supplier[0]
        color = variables.i_colour[randint(0,c_size-1)]
        if sid == "6" and color == "red":
            continue

        name = variables.i_name[randint(0,n_size-1)]

        c_key = f"{sid}_{color}_{name}"
        p_key = f"{color}_{name}"

        if c_key not in catalog:
            catalog[c_key] = (sid, p_key,  price)
            try:
                parts[p_key][2] += quantity
            except:
                parts[p_key] = (color, name, quantity)
        p_key = list(parts).index(p_key)+1

        order_data.append((len(order_data)+1, int(sid) ,p_key,quantity))
    
    #INSERT Suppliers
    supplier_data=[]
    for supplier in variables.s_data:
        sid = supplier[0]
        sname = supplier[1]
        city = supplier[2]
        street = supplier[3]

        supplier_data.append((int(sid), sname, city, street))
    sql = "INSERT INTO Suppliers (sid, sname, city, street) VALUES (%s, %s, %s, %s)"
    my_cursor.executemany(sql, supplier_data)
    print("Suppliers INSERTED")

    #INSERT Parts
    part_data = []
    for part in parts:
        pname = part
        stock_level = parts[part][2]+randint(0,10)
        color = parts[part][0]

        part_data.append((pname, stock_level, color))
    sql = "INSERT INTO Parts (pname, stock_level, color) VALUES (%s, %s, %s)"
    my_cursor.executemany(sql, part_data)
    print("Parts INSERTED")

    #INSERT Catalog
    catalog_data = []
    for item in catalog:
        sid = catalog[item][0]
        p_key = list(parts).index(catalog[item][1])+1
        unit_price = catalog[item][2]
        catalog_data.append((sid, p_key, unit_price))
    sql = "INSERT INTO Catalog (sid, sku, unit_price) VALUES (%s, %s, %s)"
    my_cursor.executemany(sql, catalog_data)
    print("Catalog INSERTED")

    #INSERT Orders
    sql = "INSERT INTO Orders (oid, sid, sku, quantity) VALUES (%s, %s, %s, %s)"
    my_cursor.executemany(sql, order_data)
    print("Orders INSERTED")