from mysql import connector
import variables
import random



def create_database(my_cursor ,name:str):
    """Create MySQL schema (database). 
    WARNING: If the schema is already present within the 
    host it will drop it and will create a new one.
    
    my_curser: CMySQLCursor
    name: alias for MySQL schema(database)
    """
    
    try:
        my_cursor.execute(f"DROP DATABASE {name}")
    except:
        print("DOESNT EXIST")
    
    my_cursor.execute(f"CREATE DATABASE {name}")
    my_cursor.execute(f"use {name}")

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
        
    catalog = {}
    order_data = []
    parts = {}

    #Sample Imput
    for x in range(size):
        #Price range 0-1
        price = random.random()
        #Quantity range per order is 1-5
        quantity = random.randint(1,5)

        supplier = random.choice(variables.s_data)
        sid = supplier[0]
        color = random.choice(variables.i_colour)
        
        #Supplier with id 6 doesnt sell red items soo we check that here
        if sid == "6" and color == "Red":
            continue

        name = random.choice(variables.i_name)

        c_key = f"{sid}_{color}_{name}"
        p_key = f"{color}_{name}"

        if c_key not in catalog:
            catalog[c_key] = (sid, p_key,  price)
            try:
                parts[p_key][2] += quantity
            except:
                parts[p_key] = (color, name, quantity)
                
        sku = list(parts).index(p_key)+1

        order_data.append((int(sid), sku, quantity))
    
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
        stock_level = parts[part][2]+random.randint(0,10)
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
    sql = "INSERT INTO Orders (sid, sku, quantity) VALUES (%s, %s, %s)"
    my_cursor.executemany(sql, order_data)
    print("Orders INSERTED")