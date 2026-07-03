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

# --- 2. productsTable (8 records, cereals only) ---
# profit_margin is excluded — it's a Calculated field in Access and derives
# automatically from buyingPrice/sellingPrice. Trying to insert it directly
# throws "field not updateable".
products = [
    (1, "Weetabix 500g", 350, 480, 60, 15),
    (2, "Cornflakes 500g", 300, 420, 55, 15),
    (3, "Oats 1kg", 250, 360, 70, 20),
    (4, "Bran Flakes 500g", 280, 390, 40, 10),
    (5, "Muesli 750g", 420, 580, 30, 10),
    (6, "Rice Krispies 400g", 320, 450, 45, 12),
    (7, "Wheat Biscuits 500g", 310, 430, 50, 12),
    (8, "Coco Pops 400g", 340, 470, 35, 10),
]
for row in products:
    cursor.execute(
        "INSERT INTO productsTable (productID, productName, buyingPrice, sellingPrice, "
        "currentStock, reorderLevel) VALUES (?, ?, ?, ?, ?, ?)",
        *row
    )

# --- 3. customersTable (8 records) ---
customers = [
    (1, "Jane", "Wanjiru", "0712345001", "2026-01-05"),
    (2, "Peter", "Otieno", "0712345002", "2026-01-06"),
    (3, "Grace", "Achieng", "0712345003", "2026-01-10"),
    (4, "Samuel", "Kiprop", "0712345004", "2026-01-12"),
    (5, "Mercy", "Njeri", "0712345005", "2026-01-15"),
    (6, "Brian", "Mutua", "0712345006", "2026-01-18"),
    (7, "Faith", "Chebet", "0712345007", "2026-01-20"),
    (8, "David", "Omondi", "0712345008", "2026-01-22"),
]
for row in customers:
    cursor.execute(
        "INSERT INTO customersTable (customerID, FirstName, lastName, PhoneNumber, DateRegistered) "
        "VALUES (?, ?, ?, ?, ?)",
        *row
    )

conn.commit()  # save parent tables before inserting rows that reference them

# --- 4. salesTable (15 records - 8 MPESA, 7 CASH) ---
sales = [
    (1, 1, 1, 2, "2026-05-04", 960, True, "QAI100234", False),
    (2, 2, 2, 1, "2026-05-04", 420, False, None, True),
    (3, 3, 3, 3, "2026-05-11", 1080, True, "QAI100455", False),
    (4, 4, 4, 2, "2026-05-11", 780, False, None, True),
    (5, 5, 5, 1, "2026-05-18", 580, True, "QAI100678", False),
    (6, 6, 6, 4, "2026-05-18", 1800, False, None, True),
    (7, 7, 7, 2, "2026-05-25", 860, True, "QAI100890", False),
    (8, 8, 8, 1, "2026-05-25", 470, False, None, True),
    (9, 1, 2, 3, "2026-06-01", 1260, True, "QAI101023", False),
    (10, 2, 3, 2, "2026-06-01", 720, False, None, True),
    (11, 3, 4, 1, "2026-06-08", 390, True, "QAI101245", False),
    (12, 4, 5, 2, "2026-06-08", 1160, False, None, True),
    (13, 5, 6, 3, "2026-06-15", 1350, True, "QAI101467", False),
    (14, 6, 7, 1, "2026-06-15", 430, False, None, True),
    (15, 7, 8, 2, "2026-06-22", 940, True, "QAI101689", False),
]
for row in sales:
    cursor.execute(
        "INSERT INTO salesTable (saleID, customer_ID, productID, quantitySold, sale_date, TotalAmount, "
        "ISMPESA, transcation_recept, IsCash) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        *row
    )

conn.commit()  # save sales before MPESATRANSACTION references them

# --- 5. MPESATRANSACTION (10 records - 8 matched, 2 unmatched) ---
mpesa_transactions = [
    (1, "QAI100234", "0712345001", 960, "2026-05-04", 1, "matched"),
    (2, "QAI100455", "0712345003", 1080, "2026-05-11", 3, "matched"),
    (3, "QAI100678", "0712345005", 580, "2026-05-18", 5, "matched"),
    (4, "QAI100890", "0712345007", 860, "2026-05-25", 7, "matched"),
    (5, "QAI101023", "0712345001", 1260, "2026-06-01", 9, "matched"),
    (6, "QAI101245", "0712345003", 390, "2026-06-08", 11, "matched"),
    (7, "QAI101467", "0712345005", 1350, "2026-06-15", 13, "matched"),
    (8, "QAI101689", "0712345007", 940, "2026-06-22", 15, "matched"),
    (9, "QAI109981", "0712399999", 650, "2026-06-25", None, "unmatched"),
    (10, "QAI109982", "0712399998", 410, "2026-06-26", None, "unmatched"),
]
for row in mpesa_transactions:
    cursor.execute(
        "INSERT INTO MPESATRANSACTION (transactionID, mpesaReceptNumber, phoneNumber, Amount, "
        "transactionDate, saleID, status_of_sale) VALUES (?, ?, ?, ?, ?, ?, ?)",
        *row
    )

# --- 6. audtTable (8 records - opening stock movements) ---
movements = [
    (1, 1, 60, "Restock", "2026-04-01"),
    (2, 2, 55, "Restock", "2026-04-01"),
    (3, 3, 70, "Restock", "2026-04-01"),
    (4, 4, 40, "Restock", "2026-04-01"),
    (5, 5, 30, "Restock", "2026-04-01"),
    (6, 6, 45, "Restock", "2026-04-01"),
    (7, 7, 50, "Restock", "2026-04-01"),
    (8, 8, 35, "Restock", "2026-04-01"),
]
for row in movements:
    cursor.execute(
        "INSERT INTO audtTable (movementID, productID, changeAmount, Reason, movementDAte) "
        "VALUES (?, ?, ?, ?, ?)",
        *row
    )

conn.commit()
cursor.close()
conn.close()

print("Mock data seeded successfully: 50 records across 6 tables.")