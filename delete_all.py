import pyodbc

DRIVER_NAME = "{Microsoft Access Driver (*.mdb, *.accdb)}"
DB_PATH = r"C:\Users\HomePC\Documents\cereal_track.accdb"  # confirm this matches your actual path

conn_str = f"DRIVER={DRIVER_NAME};DBQ={DB_PATH};"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    print("Connection successful.")
except pyodbc.Error as e:
    print("Connection failed:")
    print(e)
    raise SystemExit

# Order matters: delete child/dependent tables before parent tables,
# so nothing ever references a row that's already gone.
tables_in_delete_order = [
    "MPESATRANSACTION",   # references salesTable
    "salesTable",          # references customersTable, productsTable
    "audtTable",            # references productsTable
    "customersTable",
    "productsTable",
    "adminTable",
]

for table in tables_in_delete_order:
    cursor.execute(f"DELETE FROM {table}")
    print(f"Cleared {table}")

conn.commit()
cursor.close()
conn.close()

print("All tables cleared.")