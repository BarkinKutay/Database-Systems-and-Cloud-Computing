from mysql import connector
import scripts as run
import sys

if __name__ == "__main__":
    my_connection = connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mysql"
    )

    my_cursor = my_connection.cursor()
    print("----------------------------------------")
    try:
        my_cursor.execute("""DROP DATABASE banking""")
    except:
        print("DOESNT EXIST")

    run.create_database(my_cursor,"banking")


    #TASK 1
    run.create_tables(my_cursor)
    print("----------------------------------------")


    #TASK 2
    run.sample_imput(my_cursor,400)
    my_connection.commit()
    print("----------------------------------------")


    #TASK 3
    my_cursor.execute("""SELECT sname, COUNT(p.color) AS total
                        FROM suppliers s, parts p, catalog c
                        WHERE s.sid = c.sid
                        AND p.sku = c.sku
                        AND p.color = "red"
                        GROUP BY sname
                        ORDER BY total DESC""")
    print("{:12} {:4}".format("Name","Item Count"))
    for row in my_cursor:
         print(f"{row[0]:12} {row[1]:<4}")
    print("----------------------------------------")


    #TASK 4
    my_cursor.execute("""SELECT o.sid, s.sname, SUM(o.quantity*c.unit_price) AS total from Catalog c, Orders o, Suppliers s
    WHERE s.sid = c.sid
    AND c.sku = o.sku
    AND s.sid = o.sid
    GROUP BY o.sid
    HAVING total > 100
    ORDER BY total DESC""")
    print("{:5} {:<11}: {:20}".format("SID", "Name", "Total Oreder Value"))
    for row in my_cursor:
        print(f"{row[0]:<4} {row[1]:<12}: {round(row[2],3):<10}")
    print("----------------------------------------")

    my_cursor.close()
    my_connection.close()
