import pyodbc
DRIVER_NAME="Microsoft Access Driver (*.mdb, *.accdb)"
DB_PATH=r"C:\Users\HomePC\Documents\cereal_track.accdb"
conn_str=f"DRIVER={DRIVER_NAME};DBQ={DB_PATH};"
try:
    conn=pyodbc.connect(conn_str)
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM productsTable")
    rows=cursor.fetchall()
    if not rows:
        print("No data found in productsTable.BUt it is connected successfully")
    else:
        for row in rows:
            print(row)
            
except pyodbc.Error as e:
    print("Error in connection:")
    print(e)
finally:
    try:
        cursor.close()
        conn.close()
    except NameError:
        pass

