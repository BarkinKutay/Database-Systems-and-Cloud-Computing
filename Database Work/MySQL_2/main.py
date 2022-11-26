#Student ID: 2002044

from mysql import connector
import scripts as run
import sys

def linebreak(char="-",len=37):
    for x in range(len-1):
        print(char, end ="")
    print(char)
    
    
if __name__ == "__main__":
    """
    Can be run with arguments: 
    example: main.py data_size schema_name 
    """
    linebreak("=")
    
    schema_name = "banking"
    data_size = 400
    
    # THIS part is bugged at this point as invalid 
    # values for int and name will break it but i will 
    # leave this for later as i have other parts to clean up
    
    if len(sys.argv) >= 2:
        data_size = int(sys.argv[1])
            
    if len(sys.argv) >= 3:
        schema_name = str(sys.argv[2])
        
        
    ### START
    
    print(f"{data_size} / {schema_name}")
    
    #First we initialize the connection more detail will be present at MySQL_1
    
    my_connection = connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mysql"
    )
    my_cursor = my_connection.cursor()
    
    
    linebreak()
    
    
    run.create_database(my_cursor,schema_name)

    # Task-1: 
    # Write the DDL statements required to create the tables,
    # including appropriate primary and foreign key integrity 
    # constraints. 
    # Implement the task in python:
    
    run.create_tables(my_cursor)
    linebreak()


    # Task 2:
    # Write the DML statements to insert sample data to the tables.
    # Implement the task in python.
    
    run.sample_imput(my_cursor,data_size)
    my_connection.commit()
    linebreak()


    # Task 3:
    # Write the SQL statement to find the supplier names who supply some red part.
    # Implement the task in python. 
    
    my_cursor.execute("""
                        SELECT sname, COUNT(p.color) AS total
                        FROM suppliers s, parts p, catalog c
                        WHERE s.sid = c.sid
                        AND p.sku = c.sku
                        AND p.color = "red"
                        GROUP BY sname
                        ORDER BY total DESC
                    """)
    
    print("{:12} {:4}".format("Name","RED Item Count"))
    for row in my_cursor:
         print(f"|{row[0]:12} {row[1]:7}")

    linebreak()

    # Task 4:
    # Write the SQL statement that will return the supplier identifier, 
    # supplier name the total order value for each supplier with a 
    # total order value of at least 100.0. The value for each order is 
    # the quantity times the part’s unit price charged by that supplier. 
    # The total order value for a supplier is the sum of all the orders 
    # placed to the supplier.
    # Implement the task in python.
    
    my_cursor.execute("""
                        SELECT o.sid, s.sname, SUM(o.quantity*c.unit_price) AS total 
                        FROM Catalog c, Orders o, Suppliers s
                        WHERE s.sid = c.sid
                        AND c.sku = o.sku
                        AND s.sid = o.sid
                        GROUP BY o.sid
                        HAVING total > 100
                        ORDER BY total DESC
                    """)

    print("{:5} {:<11}: {:20}".format("SID", "Name", "Total Oreder Value"))
    for row in my_cursor:
        print(f"|{row[0]:<4} {row[1]:<12}: {round(row[2],3):<10}"
)
        
        
    linebreak()
    
    if sys.argv[len(sys.argv)-1] == "drop_db":
        my_cursor.execute(f"DROP DATABASE {schema_name}")
        print("Database droped as requested")
        
    my_cursor.close()
    my_connection.close()
    
    print("Connection closed")
    
    linebreak("=")