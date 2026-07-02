import pyodbc
import random
from datetime import date, timedelta

# --- Connection Setup (same as your test_connection.py) ---
DRIVER_NAME = "{Microsoft Access Driver (*.mdb, *.accdb)}"
DB_PATH = r"C:\Users\HomePC\Documents\cereal_track.accdb"  # confirm this matches your actual path

conn_str = f"DRIVER={DRIVER_NAME};DBQ={DB_PATH};"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


def last_id():
    """Access-specific way to get the ID just assigned by AutoNumber."""
    cursor.execute("SELECT @@IDENTITY")
    return cursor.fetchone()[0]


# --- 1. Seed Customers ---
customers = [
    ("Jane", "Wanjiru", "0712345001"),
    ("Peter", "Otieno", "0712345002"),
    ("Grace", "Achieng", "0712345003"),
    ("Samuel", "Kiprop", "0712345004"),
    ("Mercy", "Njeri", "0712345005"),
    ("Brian", "Mutua", "0712345006"),
    ("Faith", "Chebet", "0712345007"),
    ("David", "Omondi", "0712345008"),
    ("Esther", "Wambui", "0712345009"),
    ("Kevin", "Kamau", "0712345010"),
    ("Lucy", "Adhiambo", "0712345011"),
    ("Michael", "Kiplagat", "0712345012"),
]

customer_ids = []
for first, last, phone in customers:
    cursor.execute(
        "INSERT INTO customersTable (FirstName, lastName, PhoneNumber, DateRegistered) VALUES (?, ?, ?, ?)",
        first, last, phone, date.today()
    )
    customer_ids.append(last_id())

# --- 2. Seed Products (cereals only) ---
products = [
    ("Weetabix 500g", 350, 480, 60, 15),
    ("Cornflakes 500g", 300, 420, 55, 15),
    ("Oats 1kg", 250, 360, 70, 20),
    ("Bran Flakes 500g", 280, 390, 40, 10),
    ("Muesli 750g", 420, 580, 30, 10),
    ("Rice Krispies 400g", 320, 450, 45, 12),
    ("Wheat Biscuits 500g", 310, 430, 50, 12),
    ("Coco Pops 400g", 340, 470, 35, 10),
    ("Porridge Meal 1kg", 200, 300, 80, 20),
    ("Multigrain Flakes 500g", 360, 500, 25, 10),
]

product_ids = []
for name, buy, sell, stock, reorder in products:
    cursor.execute(
        "INSERT INTO productsTable (productName, buyingPrice, sellingPrice, currentStock, reorderLevel) "
        "VALUES (?, ?, ?, ?, ?)",
        name, buy, sell, stock, reorder
    )
    product_ids.append(last_id())

conn.commit()  # save customers/products before building sales that reference them

# --- 3. Seed Sales spread across several weeks ---
today = date.today()
sale_ids_and_dates = []

for week_offset in range(16):  # 16 weeks of history for a larger dataset
    week_start = today - timedelta(weeks=week_offset)

    for _ in range(random.randint(8, 15)):  # more sales per week
        sale_date = week_start - timedelta(days=random.randint(0, 6))  # spread across days in the week
        cust_id = random.choice(customer_ids)
        prod_id = random.choice(product_ids)
        qty = random.randint(1, 5)

        # find that product's sellingPrice to compute TotalAmount
        cursor.execute("SELECT sellingPrice FROM productsTable WHERE productID = ?", prod_id)
        selling_price = cursor.fetchone()[0]
        total = qty * selling_price

        is_mpesa = random.choice([True, False])

        if is_mpesa:
            receipt = f"QAI{random.randint(100000, 999999)}"
            cursor.execute(
                "INSERT INTO salesTable (customer_ID, productID, quantitySold, sale_date, TotalAmount, "
                "IsMPESA, transcation_recept, IsCash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                cust_id, prod_id, qty, sale_date, total, True, receipt, False
            )
        else:
            cursor.execute(
                "INSERT INTO salesTable (customer_ID, productID, quantitySold, sale_date, TotalAmount, "
                "IsMPESA, transcation_recept, IsCash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                cust_id, prod_id, qty, sale_date, total, False, None, True
            )

        sale_id = last_id()
        sale_ids_and_dates.append((sale_id, sale_date, is_mpesa, receipt if is_mpesa else None, cust_id))

conn.commit()

# --- 4. Seed matching MPESA transactions for MPESA sales ---
for sale_id, sale_date, is_mpesa, receipt, cust_id in sale_ids_and_dates:
    if not is_mpesa:
        continue

    cursor.execute("SELECT PhoneNumber FROM customersTable WHERE customerID = ?", cust_id)
    phone = cursor.fetchone()[0]

    cursor.execute("SELECT TotalAmount FROM salesTable WHERE saleID = ?", sale_id)
    amount = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO MPESATRANSACTION (mpesaReceptNumber, phoneNumber, Amount, transactionDate, saleID, Status) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        receipt, phone, amount, sale_date, sale_id, "Matched"
    )

# --- 5. A handful of deliberately Unmatched transactions, to test that query too ---
for _ in range(8):
    cursor.execute(
        "INSERT INTO MPESATRANSACTION (mpesaReceptNumber, phoneNumber, Amount, transactionDate, saleID, Status) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        f"QAI{random.randint(100000, 999999)}", "0712399999", random.randint(300, 900),
        today, None, "Unmatched"
    )

conn.commit()
cursor.close()
conn.close()

print("Mock data seeded successfully.")
