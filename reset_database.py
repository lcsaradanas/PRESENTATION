import sqlite3
import os
import time

print("Starting database reset script...")

# Delete the existing database file if it exists
if os.path.exists('donationdriveDBMS.db'):
    print(f"Found existing database, deleting it...")
    try:
        # Close any open connections
        try:
            conn = sqlite3.connect('donationdriveDBMS.db')
            conn.close()
        except:
            pass

        # Try to delete it a few times in case of file locks
        for i in range(5):
            try:
                os.remove('donationdriveDBMS.db')
                print("Database file deleted successfully.")
                break
            except Exception as e:
                print(f"Error deleting database file (attempt {i + 1}): {e}")
                time.sleep(1)  # wait a bit before retrying
    except Exception as e:
        print(f"Final error deleting database: {e}")

# Create new database
print("Creating new database...")
conn = sqlite3.connect('donationdriveDBMS.db')
cursor = conn.cursor()

# Create tables
print("Creating tables...")

# Create accounts table
cursor.execute('''
               CREATE TABLE accounts
               (
                   user_code  VARCHAR(10) PRIMARY KEY,
                   username   VARCHAR NOT NULL,
                   firstname  VARCHAR NOT NULL,
                   lastname   VARCHAR NOT NULL,
                   password   VARCHAR NOT NULL,
                   cpassword  VARCHAR NOT NULL,
                   typeofUser BOOLEAN NOT NULL
               )
               ''')

# Create location_info table
cursor.execute('''
               CREATE TABLE location_info
               (
                   location_id   VARCHAR(2) PRIMARY KEY,
                   location_name VARCHAR(50) NOT NULL
               )
               ''')

# Create org_info table
cursor.execute('''
               CREATE TABLE org_info
               (
                   org_id      INTEGER PRIMARY KEY,
                   name        VARCHAR(50) NOT NULL,
                   user_code   VARCHAR(10) NOT NULL,
                   location_id VARCHAR(2)  NOT NULL,
                   FOREIGN KEY (user_code) REFERENCES accounts (user_code),
                   FOREIGN KEY (location_id) REFERENCES location_info (location_id)
               )
               ''')

# Create food_list table
cursor.execute('''
               CREATE TABLE food_list
               (
                   foodList_id INTEGER PRIMARY KEY,
                   name        VARCHAR(50) NOT NULL,
                   description TEXT
               )
               ''')

# Create products table
cursor.execute('''
               CREATE TABLE products
               (
                   product_id INTEGER PRIMARY KEY,
                   product    VARCHAR NOT NULL,
                   perishable BOOLEAN NOT NULL,
                   quantity   INTEGER(20) NOT NULL
               )
               ''')

# Create link_list table (joining table between food_list and products)
cursor.execute('''
               CREATE TABLE link_list
               (
                   foodList_id INTEGER NOT NULL,
                   product_id  INTEGER NOT NULL,
                   PRIMARY KEY (foodList_id, product_id),
                   FOREIGN KEY (foodList_id) REFERENCES food_list (foodList_id),
                   FOREIGN KEY (product_id) REFERENCES products (product_id)
               )
               ''')

# Create delivery table
cursor.execute('''
               CREATE TABLE delivery
               (
                   delivery_id    INTEGER PRIMARY KEY,
                   departure_time TIME,
                   date           DATE       NOT NULL,
                   foodList_id    INTEGER    NOT NULL,
                   location_id    VARCHAR(2) NOT NULL,
                   org_id         INTEGER    NOT NULL,
                   FOREIGN KEY (foodList_id) REFERENCES food_list (foodList_id),
                   FOREIGN KEY (location_id) REFERENCES location_info (location_id),
                   FOREIGN KEY (org_id) REFERENCES org_info (org_id)
               )
               ''')

# Create donation_info table
cursor.execute('''
               CREATE TABLE donation_info
               (
                   donation_id INTEGER PRIMARY KEY,
                   user_code   VARCHAR(10) NOT NULL,
                   FOREIGN KEY (user_code) REFERENCES accounts (user_code)
               )
               ''')

# Commit the table creation
conn.commit()
print("Tables created successfully")

# Add default data
print("Adding default data...")

# Add default locations
locations = [
    ("MN", "Manila"),
    ("QC", "Quezon City"),
    ("CL", "Caloocan"),
    ("MK", "Makati"),
    ("PA", "Pasay"),
    ("TA", "Taguig"),
    ("MM", "Marikina"),
    ("PQ", "Parañaque"),
    ("MU", "Muntinlupa"),
    ("VC", "Valenzuela")
]

for loc_id, loc_name in locations:
    cursor.execute(
        "INSERT INTO location_info (location_id, location_name) VALUES (?, ?)",
        (loc_id, loc_name)
    )

# Add default admin account
cursor.execute(
    "INSERT INTO accounts (user_code, username, firstname, lastname, password, cpassword, typeofUser) VALUES (?, ?, ?, ?, ?, ?, ?)",
    ('ADMIN123456', 'admin_pedro', 'Pedro', 'Garcia', 'password123', 'password123', 1)
)

# Add default user account
cursor.execute(
    "INSERT INTO accounts (user_code, username, firstname, lastname, password, cpassword, typeofUser) VALUES (?, ?, ?, ?, ?, ?, ?)",
    ('OTOOS2MJY4', 'ngo_careph', 'Marco', 'Reyes', 'password123', 'password123', 0)
)

# Add an organization for the user
cursor.execute(
    "INSERT INTO org_info (org_id, name, user_code, location_id) VALUES (?, ?, ?, ?)",
    (1, 'CARE Philippines', 'OTOOS2MJY4', 'QC')
)

# Add default food lists
food_lists_data = [
    (1, "Food List 1 - For Closest Location", "Food items for organizations in closest locations"),
    (2, "Food List 2 - For Near Location", "Food items for organizations in near locations"),
    (3, "Food List 3 - For Average Distance", "Food items for organizations in average distance"),
    (4, "Food List 4 - For Far Location", "Food items for organizations in far locations"),
    (5, "Food List 5 - For Farthest Location", "Food items for organizations in farthest locations")
]

for food_list in food_lists_data:
    cursor.execute(
        "INSERT INTO food_list (foodList_id, name, description) VALUES (?, ?, ?)",
        food_list
    )

# Add some sample products
products = [
    (1, "Rice", 0, 1000),
    (2, "Canned Goods", 0, 500),
    (3, "Bread", 1, 200),
    (4, "Milk", 1, 300),
    (5, "Bottled Water", 0, 1000)
]

for product in products:
    cursor.execute(
        "INSERT INTO products (product_id, product, perishable, quantity) VALUES (?, ?, ?, ?)",
        product
    )

# Add sample delivery
cursor.execute(
    "INSERT INTO delivery (delivery_id, departure_time, date, foodList_id, location_id, org_id) VALUES (?, ?, ?, ?, ?, ?)",
    (1, '09:00', '2025-05-12', 1, 'QC', 1)
)

# Commit all the default data
conn.commit()

print("Default data added successfully")

# Verify the database content
print("\nVerifying database content:")

print("\nAccounts:")
cursor.execute("SELECT * FROM accounts")
accounts = cursor.fetchall()
for account in accounts:
    print(account)

print("\nLocations:")
cursor.execute("SELECT * FROM location_info")
locations = cursor.fetchall()
for location in locations:
    print(location)

print("\nOrganizations:")
cursor.execute("SELECT * FROM org_info")
orgs = cursor.fetchall()
for org in orgs:
    print(org)

print("\nFood Lists:")
cursor.execute("SELECT * FROM food_list")
food_lists = cursor.fetchall()
for food_list in food_lists:
    print(food_list)

print("\nProducts:")
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()
for product in products:
    print(product)

print("\nDeliveries:")
cursor.execute("SELECT * FROM delivery")
deliveries = cursor.fetchall()
for delivery in deliveries:
    print(delivery)

# Close the connection
conn.close()

print("\nDatabase reset completed successfully!") 