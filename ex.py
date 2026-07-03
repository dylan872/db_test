import pyodbc

# --- Connection Setup ---
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
    raise SystemExit  # stop here if we can't even connect


# --- 1. adminTable (1 record) ---
cursor.execute(
    "INSERT INTO adminTable (adminID, businessName, pochiNumber, dateActivated) VALUES (?, ?, ?, ?)",
    1, "Cereal Board PoS", "174379", "2026-01-01"
    
)
conn.commit()  # Commit after each major insert block to ensure data is saved