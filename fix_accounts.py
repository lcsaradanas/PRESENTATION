import sqlite3
import os

print("Starting database fix script...")

try:
    # Connect to the database
    print("Connecting to database...")
    conn = sqlite3.connect('donationdriveDBMS.db')
    cursor = conn.cursor()

    print("Connected successfully.")

    # Debug database file
    if os.path.exists('donationdriveDBMS.db'):
        print(f"Database file exists, size: {os.path.getsize('donationdriveDBMS.db')} bytes")
    else:
        print("Database file does not exist!")
        # Create a new database file
        conn = sqlite3.connect('donationdriveDBMS.db')
        cursor = conn.cursor()
        print("Created new database file")

    print("Checking accounts table...")
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
        if not cursor.fetchone():
            print("Accounts table doesn't exist! Creating it...")
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS accounts
                           (
                               user_code
                               VARCHAR
                           (
                               10
                           ) PRIMARY KEY,
                               username VARCHAR NOT NULL,
                               firstname VARCHAR NOT NULL,
                               lastname VARCHAR NOT NULL,
                               password VARCHAR NOT NULL,
                               cpassword VARCHAR NOT NULL,
                               typeofUser BOOLEAN NOT NULL
                               )
                           ''')
            conn.commit()
            print("Accounts table created")
    except Exception as e:
        print(f"Error checking tables: {e}")

    try:
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts found in the database!")
        else:
            print(f"Found {len(accounts)} accounts:")
            for account in accounts:
                print(account)
    except Exception as e:
        print(f"Error checking accounts: {e}")

    # Check if admin_pedro exists
    try:
        cursor.execute("SELECT * FROM accounts WHERE username = 'admin_pedro'")
        admin = cursor.fetchone()

        if not admin:
            print("\nRecreating admin account...")
            cursor.execute(
                "INSERT INTO accounts (user_code, username, firstname, lastname, password, cpassword, typeofUser) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ('ADMIN123456', 'admin_pedro', 'Pedro', 'Garcia', 'password123', 'password123', 1)
            )
            conn.commit()
            print("Admin account created successfully")
        else:
            print("Admin account exists:", admin)
    except Exception as e:
        print(f"Error with admin account: {e}")

    # Check if ngo_careph exists
    try:
        cursor.execute("SELECT * FROM accounts WHERE username = 'ngo_careph'")
        user = cursor.fetchone()

        if not user:
            print("\nRecreating user account...")
            cursor.execute(
                "INSERT INTO accounts (user_code, username, firstname, lastname, password, cpassword, typeofUser) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ('OTOOS2MJY4', 'ngo_careph', 'Marco', 'Reyes', 'password123', 'password123', 0)
            )
            conn.commit()
            print("User account created successfully")

            # Check for organization table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='org_info'")
            if not cursor.fetchone():
                print("org_info table doesn't exist! Creating it...")
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS org_info
                               (
                                   org_id
                                   INTEGER
                                   PRIMARY
                                   KEY,
                                   name
                                   VARCHAR
                               (
                                   50
                               ) NOT NULL,
                                   user_code VARCHAR
                               (
                                   10
                               ) NOT NULL,
                                   location_id VARCHAR
                               (
                                   2
                               ) NOT NULL
                                   )
                               ''')
                conn.commit()
                print("org_info table created")

                # Create location table if needed
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='location_info'")
                if not cursor.fetchone():
                    print("location_info table doesn't exist! Creating it...")
                    cursor.execute('''
                                   CREATE TABLE IF NOT EXISTS location_info
                                   (
                                       location_id
                                       VARCHAR
                                   (
                                       2
                                   ) PRIMARY KEY,
                                       location_name VARCHAR
                                   (
                                       50
                                   ) NOT NULL
                                       )
                                   ''')
                    conn.commit()
                    print("location_info table created")

                    # Add default locations
                    locations = [
                        ("MN", "Manila"),
                        ("QC", "Quezon City"),
                        ("CL", "Caloocan"),
                        ("MK", "Makati"),
                        ("PA", "Pasay")
                    ]
                    for loc_id, loc_name in locations:
                        cursor.execute(
                            "INSERT INTO location_info (location_id, location_name) VALUES (?, ?)",
                            (loc_id, loc_name)
                        )
                    conn.commit()
                    print("Default locations added")

            # Check if org exists for this user
            cursor.execute("SELECT * FROM org_info WHERE user_code = 'OTOOS2MJY4'")
            org = cursor.fetchone()

            if not org:
                print("Adding organization for user...")
                cursor.execute(
                    "INSERT INTO org_info (org_id, name, user_code, location_id) VALUES (?, ?, ?, ?)",
                    (2, 'CARE Philippines', 'OTOOS2MJY4', 'QC')
                )
                conn.commit()
                print("Organization added successfully")
        else:
            print("User account exists:", user)

            # Check if org exists for this user
            user_code = user[0]
            cursor.execute("SELECT * FROM org_info WHERE user_code = ?", (user_code,))
            org = cursor.fetchone()

            if not org:
                print(f"Adding missing organization for user code: {user_code}")
                cursor.execute(
                    "INSERT INTO org_info (org_id, name, user_code, location_id) VALUES (?, ?, ?, ?)",
                    (2, 'CARE Philippines', user_code, 'QC')
                )
                conn.commit()
                print("Organization added successfully")
            else:
                print("Organization exists for user:", org)
    except Exception as e:
        print(f"Error with user account: {e}")

    print("\nAfter fixes - Accounts:")
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    for account in accounts:
        print(account)

    print("\nOrganizations:")
    cursor.execute("SELECT * FROM org_info")
    orgs = cursor.fetchall()
    for org in orgs:
        print(org)

    # Add product lists
    print("\nChecking food lists...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='food_list'")
    if not cursor.fetchone():
        print("food_list table doesn't exist! Creating it...")
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS food_list
                       (
                           foodList_id
                           INTEGER
                           PRIMARY
                           KEY,
                           name
                           VARCHAR
                       (
                           50
                       ) NOT NULL,
                           description TEXT
                           )
                       ''')
        conn.commit()
        print("food_list table created")

    cursor.execute("SELECT * FROM food_list")
    food_lists = cursor.fetchall()

    if not food_lists:
        print("No food lists found. Creating default food lists...")
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
        conn.commit()
        print("Default food lists created")
    else:
        print(f"Found {len(food_lists)} food lists:")
        for food_list in food_lists:
            print(food_list)

    conn.close()
    print("\nDatabase fixed successfully!")
except Exception as e:
    print(f"ERROR in script: {e}") 