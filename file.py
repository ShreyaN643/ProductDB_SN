import pyodbc
# ==============================================
# Database Connection
# ==============================================
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=SHREYA-PC\SQLEXPRESS;'
    'DATABASE=ProductDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
# ==============================================
# Ensure Table Exists
# ==============================================
create_table_query = '''
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Product' AND xtype='U')
CREATE TABLE Product (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(100),
    Price DECIMAL(10,2),
    Quantity INT
)
'''
cursor.execute(create_table_query)
conn.commit()
print(":white_check_mark: Table 'Product' is ready.\n")
# ==============================================
# Helper Functions
# ==============================================
def show_menu():
    print("\n:clipboard: PRODUCT MANAGEMENT MENU")
    print(":one:  Insert New Product")
    print(":two:  View All Products")
    # print(":three:  Update Product")   # temporarily disabled
    # print(":four:  Delete Product")   # temporarily disabled
    print(":five:  Search Products")
    print(":six:  Exit")
def view_products():
    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()
    if not rows:
        print(":warning: No products found.")
    else:
        print("\n:package: Product Table Data:")
        for row in rows:
            print(f"ID: {row.ProductID}, Name: {row.ProductName}, Price: {row.Price}, Quantity: {row.Quantity}")
def insert_product():
    name = input("Enter Product Name: ").strip()
    price = float(input("Enter Price: "))
    quantity = int(input("Enter Quantity: "))
    cursor.execute("INSERT INTO Product (ProductName, Price, Quantity) VALUES (?, ?, ?)", (name, price, quantity))
    conn.commit()
    print(f":white_check_mark: '{name}' inserted successfully!")
# ----------------------------------------------
# The following functions are commented out for now
# ----------------------------------------------
"""
def update_product():
    view_products()
    pid = input("\nEnter Product ID to update: ")
    new_price = float(input("Enter new Price: "))
    new_quantity = int(input("Enter new Quantity: "))
    cursor.execute("UPDATE Product SET Price = ?, Quantity = ? WHERE ProductID = ?", (new_price, new_quantity, pid))
    conn.commit()
    print(f":arrows_counterclockwise: Product ID {pid} updated successfully!")
def delete_product():
    view_products()
    pid = input("\nEnter Product ID to delete: ")
    cursor.execute("DELETE FROM Product WHERE ProductID = ?", (pid,))
    conn.commit()
    print(f":wastebasket: Product ID {pid} deleted successfully!")
"""
# ==============================================
# Search Functionality
# ==============================================
def search_products():
    print("\n:mag: SEARCH OPTIONS")
    print(":one:  Search by Product Name")
    print(":two:  Search by Price Range")
    print(":three:  Search by Quantity Range")
    choice = input("Enter your choice (1–3): ").strip()
    if choice == '1':
        name = input("Enter product name (partial or full): ").strip()
        cursor.execute("SELECT * FROM Product WHERE ProductName LIKE ?", ('%' + name + '%',))
    elif choice == '2':
        min_price = float(input("Enter minimum price: "))
        max_price = float(input("Enter maximum price: "))
        cursor.execute("SELECT * FROM Product WHERE Price BETWEEN ? AND ?", (min_price, max_price))
    elif choice == '3':
        min_qty = int(input("Enter minimum quantity: "))
        max_qty = int(input("Enter maximum quantity: "))
        cursor.execute("SELECT * FROM Product WHERE Quantity BETWEEN ? AND ?", (min_qty, max_qty))
    else:
        print(":x: Invalid search option.")
        return
    rows = cursor.fetchall()
    if not rows:
        print(":warning: No products match your search criteria.")
    else:
        print("\n:package: Search Results:")
        for row in rows:
            print(f"ID: {row.ProductID}, Name: {row.ProductName}, Price: {row.Price}, Quantity: {row.Quantity}")
# ==============================================
# Main Program Loop
# ==============================================
while True:
    show_menu()
    choice = input("\nEnter your choice (1–6): ").strip()
    if choice == '1':
        insert_product()
    elif choice == '2':
        view_products()
    # elif choice == '3':
    #     update_product()
    # elif choice == '4':
    #     delete_product()
    elif choice == '5':
        search_products()
    elif choice == '6':
        print(":wave: Exiting program...")
        break
    else:
        print(":x: Invalid choice. Please enter 1–6.")
# ==============================================
# Close Connection
# ==============================================
cursor.close()
conn.close()
print(":lock: Connection closed successfully.")