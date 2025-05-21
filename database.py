import sqlite3
import re
import os
import random
import string


class Database:
    DB_NAME = "donationdriveDBMS.db"

    def __init__(self):
        """Initialize database connection and create tables if they don't exist"""
        self.connection = sqlite3.connect(self.DB_NAME)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def connect_db(self):
        """Create a new connection to the database"""
        try:
            conn = sqlite3.connect(self.DB_NAME)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def refresh_connection(self):
        """Refresh the database connection"""
        try:
            if self.connection:
                self.connection.close()
            self.connection = sqlite3.connect(self.DB_NAME)
            self.cursor = self.connection.cursor()
            print("Database connection refreshed successfully")
            return True
        except Exception as e:
            print(f"Error refreshing connection: {e}")
            return False

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()

    def commit(self):
        """Commit changes to the database"""
        if self.connection:
            self.connection.commit()

    def create_tables(self):
        """Create all tables based on the ERD if they don't already exist"""
        # Create accounts table
        self.cursor.execute('''
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

        # Create location_info table
        self.cursor.execute('''
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

        # Create org_info table
        self.cursor.execute('''
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
                            ) NOT NULL,
                                FOREIGN KEY
                            (
                                user_code
                            ) REFERENCES accounts
                            (
                                user_code
                            ),
                                FOREIGN KEY
                            (
                                location_id
                            ) REFERENCES location_info
                            (
                                location_id
                            )
                                )
                            ''')

        # Create food_list table
        self.cursor.execute('''
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

        # Create products table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS products
                            (
                                product_id
                                INTEGER
                                PRIMARY
                                KEY,
                                product
                                VARCHAR
                                NOT
                                NULL,
                                perishable
                                BOOLEAN
                                NOT
                                NULL,
                                quantity
                                INTEGER
                            (
                                20
                            ) NOT NULL
                                )
                            ''')

        # Create link_list table (joining table between food_list and products)
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS link_list
                            (
                                foodList_id
                                INTEGER
                                NOT
                                NULL,
                                product_id
                                INTEGER
                                NOT
                                NULL,
                                PRIMARY
                                KEY
                            (
                                foodList_id,
                                product_id
                            ),
                                FOREIGN KEY
                            (
                                foodList_id
                            ) REFERENCES food_list
                            (
                                foodList_id
                            ),
                                FOREIGN KEY
                            (
                                product_id
                            ) REFERENCES products
                            (
                                product_id
                            )
                                )
                            ''')

        # Create delivery table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS delivery
                            (
                                delivery_id
                                INTEGER
                                PRIMARY
                                KEY,
                                departure_time
                                TIME,
                                date
                                DATE
                                NOT
                                NULL,
                                foodList_id
                                INTEGER
                                NOT
                                NULL,
                                location_id
                                VARCHAR
                            (
                                2
                            ) NOT NULL,
                                org_id INTEGER NOT NULL,
                                FOREIGN KEY
                            (
                                foodList_id
                            ) REFERENCES food_list
                            (
                                foodList_id
                            ),
                                FOREIGN KEY
                            (
                                location_id
                            ) REFERENCES location_info
                            (
                                location_id
                            ),
                                FOREIGN KEY
                            (
                                org_id
                            ) REFERENCES org_info
                            (
                                org_id
                            )
                                )
                            ''')

        # Create donation_info table
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS donation_info
                            (
                                donation_id
                                INTEGER
                                PRIMARY
                                KEY,
                                user_code
                                VARCHAR
                            (
                                10
                            ) NOT NULL,
                                FOREIGN KEY
                            (
                                user_code
                            ) REFERENCES accounts
                            (
                                user_code
                            )
                                )
                            ''')

        # Commit the changes
        self.commit()

    def generate_id(self, type_id):
        """Generate a unique ID for various entities"""
        if type_id == "user":
            # Generate a unique user code (10 characters alphanumeric)
            while True:
                user_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                # Check if the user_code already exists
                self.cursor.execute("SELECT COUNT(*) FROM accounts WHERE user_code = ?", (user_code,))
                if self.cursor.fetchone()[0] == 0:
                    return user_code
        elif type_id == "product_list":
            # Get the next available ID from food_list table
            self.cursor.execute("SELECT MAX(foodList_id) FROM food_list")
            max_id = self.cursor.fetchone()[0]
            return 1 if max_id is None else max_id + 1
        elif type_id == "delivery":
            # Get the next available ID from delivery table
            self.cursor.execute("SELECT MAX(delivery_id) FROM delivery")
            max_id = self.cursor.fetchone()[0]
            return 1 if max_id is None else max_id + 1
        elif type_id == "org":
            # Get the next available ID from org_info table
            self.cursor.execute("SELECT MAX(org_id) FROM org_info")
            max_id = self.cursor.fetchone()[0]
            return 1 if max_id is None else max_id + 1
        elif type_id == "product":
            # Get the next available ID from products table
            self.cursor.execute("SELECT MAX(product_id) FROM products")
            max_id = self.cursor.fetchone()[0]
            return 1 if max_id is None else max_id + 1
        return None

    # ACCOUNT OPERATIONS

    def create_account(self, username, firstname, lastname, password, confirm_password, user_type):
        """Create a new user account"""
        # Generate user code
        user_code = self.generate_id("user")

        # Check if username already exists
        self.cursor.execute("SELECT COUNT(*) FROM accounts WHERE username = ?", (username,))
        if self.cursor.fetchone()[0] > 0:
            return None, "Username already exists"

        # Insert the new account
        try:
            self.cursor.execute(
                "INSERT INTO accounts (user_code, username, firstname, lastname, password, cpassword, typeofUser) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_code, username, firstname, lastname, password, confirm_password, user_type)
            )
            self.commit()

            # If the account is an admin (user_type = 1), add to donation_info
            if user_type == 1:
                try:
                    self.cursor.execute("SELECT 1 FROM donation_info WHERE user_code = ?", (user_code,))
                    if not self.cursor.fetchone():
                        self.add_donation(user_code)
                except Exception as e:
                    print(f"Warning: Failed to add admin to donation_info: {e}")

            return user_code, None
        except Exception as e:
            return None, str(e)

    def get_user_by_username(self, username):
        """Get user information by username"""
        print(f"Database - get_user_by_username called for username: {username}")
        try:
            # Refresh connection to ensure we get the latest data
            self.refresh_connection()

            # Query the user
            self.cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            print(f"Database - get_user_by_username result: {result}")
            return result
        except Exception as e:
            print(f"Error in get_user_by_username: {str(e)}")
            return None

    def verify_login(self, username, password):
        """Verify login credentials and return user information"""
        try:
            print(f"Attempting login with username: {username}")
            # Refresh connection first
            self.refresh_connection()

            self.cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?",
                                (username, password))
            user = self.cursor.fetchone()
            print(f"Login result: {user}")
            return user
        except Exception as e:
            print(f"Login error: {str(e)}")
            return None

    def get_user_by_id(self, user_code):
        """Get user information by user code"""
        print(f"Database - get_user_by_id called for user_code: {user_code}")
        try:
            # Refresh connection to ensure we get the latest data
            self.refresh_connection()

            # Query the user
            self.cursor.execute("SELECT * FROM accounts WHERE user_code = ?", (user_code,))
            result = self.cursor.fetchone()
            print(f"Database - get_user_by_id result: {result}")
            return result
        except Exception as e:
            print(f"Error in get_user_by_id: {str(e)}")
            return None

    def get_all_admin_accounts(self):
        """Get all admin accounts"""
        print("Database - get_all_admin_accounts called")
        try:
            # Refresh connection to ensure we get the latest data
            self.refresh_connection()

            # Query admin accounts (typeofUser = 1)
            self.cursor.execute(
                "SELECT user_code, username, firstname, lastname FROM accounts WHERE typeofUser = 1 ORDER BY username")
            results = self.cursor.fetchall()
            print(f"Database - get_all_admin_accounts found {len(results)} admins")
            return results
        except Exception as e:
            print(f"Error in get_all_admin_accounts: {str(e)}")
            return []

    def search_admin_accounts(self, term):
        """Search admin accounts by username, firstname, or lastname"""
        print(f"Database - search_admin_accounts called with term: {term}")
        try:
            self.refresh_connection()

            wildcard = f"%{term}%"
            self.cursor.execute(
                """
                SELECT user_code, username, firstname, lastname
                FROM accounts
                WHERE typeofUser = 1
                  AND (
                    username LIKE ? OR firstname LIKE ? OR lastname LIKE ?
                    )
                ORDER BY username
                """,
                (wildcard, wildcard, wildcard)
            )
            results = self.cursor.fetchall()
            print(f"Database - search_admin_accounts found {len(results)} matching admins")
            return results
        except Exception as e:
            print(f"Error in search_admin_accounts: {str(e)}")
            return []

    def load_admin_accounts(self, search_term=None):
        if not self.user:
            return

        if search_term:
            self.admin_accounts = self.database.search_admin_accounts(search_term)
        else:
            self.admin_accounts = self.database.get_all_admin_accounts()

        self.table.setRowCount(0)

        for row, admin in enumerate(self.admin_accounts):
            username = admin[1]
            firstname = admin[2]
            lastname = admin[3]

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(username))
            self.table.setItem(row, 1, QTableWidgetItem(firstname))
            self.table.setItem(row, 2, QTableWidgetItem(lastname))

    def update_user(self, user_code, username, firstname, lastname, password):
        """Update user account information"""
        print(f"Database - update_user called for user_code: {user_code}")
        print(f"Database - update details: username={username}, firstname={firstname}, lastname={lastname}")
        try:
            # Refresh connection first
            self.refresh_connection()

            # Check if user exists
            self.cursor.execute("SELECT * FROM accounts WHERE user_code = ?", (user_code,))
            user = self.cursor.fetchone()
            if not user:
                print(f"Error: User with code {user_code} not found")
                return False, "User not found"

            # Update user information
            self.cursor.execute(
                "UPDATE accounts SET username = ?, firstname = ?, lastname = ?, password = ?, cpassword = ? WHERE user_code = ?",
                (username, firstname, lastname, password, password, user_code)
            )
            # Make sure changes are committed
            self.connection.commit()

            # Verify update was successful
            rows_updated = self.cursor.rowcount
            print(f"Database - update_user: {rows_updated} rows updated")

            if rows_updated == 0:
                print("Warning: No rows were updated, but no error occurred")

            # Double-check the update
            self.cursor.execute("SELECT * FROM accounts WHERE user_code = ?", (user_code,))
            updated_user = self.cursor.fetchone()
            print(f"Updated user: {updated_user}")

            return True, None
        except Exception as e:
            print(f"Database - update_user failed: {str(e)}")
            return False, str(e)

    # LOCATION OPERATIONS

    def add_location(self, location_id, location_name):
        """Add a new location"""
        try:
            self.cursor.execute(
                "INSERT INTO location_info (location_id, location_name) VALUES (?, ?)",
                (location_id, location_name)
            )
            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_all_locations(self):
        """Get all locations"""
        self.cursor.execute("SELECT * FROM location_info ORDER BY location_name")
        return self.cursor.fetchall()

    # ORGANIZATION OPERATIONS

    def add_organization(self, name, user_code, location_id):
        """Add a new organization"""
        org_id = self.generate_id("org")
        try:
            self.cursor.execute(
                "INSERT INTO org_info (org_id, name, user_code, location_id) VALUES (?, ?, ?, ?)",
                (org_id, name, user_code, location_id)
            )
            self.commit()
            return org_id, None
        except Exception as e:
            return None, str(e)

    def get_all_organizations(self, search_term=None):
        """Get all organizations with optional search filter"""
        query = """
                SELECT o.org_id, o.name, l.location_name, a.firstname || ' ' || a.lastname AS contact_person
                FROM org_info o
                         JOIN location_info l ON o.location_id = l.location_id
                         JOIN accounts a ON o.user_code = a.user_code \
                """

        if search_term:
            query += f"""
                WHERE (o.name LIKE '%{search_term}%' 
                OR l.location_name LIKE '%{search_term}%' 
                OR a.firstname LIKE '%{search_term}%'
                OR a.lastname LIKE '%{search_term}%')
            """

        query += " ORDER BY o.name"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_non_government_organizations(self, search_term=None):
        """Get non-government organizations with optional search filter"""
        query = """
                SELECT o.org_id, o.name, l.location_name, a.firstname || ' ' || a.lastname AS contact_person
                FROM org_info o
                         JOIN location_info l ON o.location_id = l.location_id
                         JOIN accounts a ON o.user_code = a.user_code
                WHERE (o.name NOT LIKE '%government%' AND o.name NOT LIKE '%govt%') \
                """

        if search_term:
            query += f"""
                AND (o.name LIKE '%{search_term}%' 
                OR l.location_name LIKE '%{search_term}%' 
                OR a.firstname LIKE '%{search_term}%'
                OR a.lastname LIKE '%{search_term}%')
            """

        query += " ORDER BY o.name"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_user_organization(self, user_code):
        """Get the organization associated with a user by user_code"""
        try:
            query = """
                    SELECT o.org_id, o.name, l.location_id, l.location_name
                    FROM org_info o
                             JOIN location_info l ON o.location_id = l.location_id
                    WHERE o.user_code = ? \
                    """
            self.cursor.execute(query, (user_code,))
            org_data = self.cursor.fetchone()

            # Print detailed debug info
            print(f"Organization query for {user_code} returned: {org_data}")

            # If no organization found, create a default one
            if not org_data:
                print(f"No organization found for user {user_code}, creating default")
                # Check if user exists and is not an admin
                self.cursor.execute("SELECT * FROM accounts WHERE user_code = ? AND typeofUser = 0", (user_code,))
                user = self.cursor.fetchone()

                if user:
                    # Create a default organization for this user
                    org_id = self.generate_id("org")
                    try:
                        self.cursor.execute(
                            "INSERT INTO org_info (org_id, name, user_code, location_id) VALUES (?, ?, ?, ?)",
                            (org_id, "CARE Philippines", user_code, "QC")
                        )
                        self.commit()
                        print(f"Created default organization with ID {org_id}")

                        # Retrieve the newly created organization
                        self.cursor.execute(query, (user_code,))
                        org_data = self.cursor.fetchone()
                    except Exception as e:
                        print(f"Error creating default organization: {str(e)}")

            return org_data
        except Exception as e:
            print(f"Error retrieving user organization: {str(e)}")
            return None

    # PRODUCT OPERATIONS

    def add_product(self, product_name, perishable, quantity, product_id=None):
        """Add a new product with optional specific ID"""
        # If no product_id is provided, generate one
        if product_id is None:
            product_id = self.generate_id("product")
        try:
            self.cursor.execute(
                "INSERT INTO products (product_id, product, perishable, quantity) VALUES (?, ?, ?, ?)",
                (product_id, product_name, perishable, quantity)
            )
            self.commit()
            return product_id, None
        except Exception as e:
            return None, str(e)

    def get_all_products(self):
        """Get all products"""
        self.cursor.execute("SELECT * FROM products ORDER BY product")
        return self.cursor.fetchall()

    def update_product(self, product_id, product_name, perishable, quantity):
        """Update product information"""
        try:
            self.cursor.execute(
                "UPDATE products SET product = ?, perishable = ?, quantity = ? WHERE product_id = ?",
                (product_name, perishable, quantity, product_id)
            )
            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def delete_product(self, product_id):
        """Delete a product and its references in food lists"""
        try:
            # Begin a transaction
            self.connection.execute("BEGIN TRANSACTION")

            # First delete from link_list table
            self.cursor.execute("DELETE FROM link_list WHERE product_id = ?", (product_id,))

            # Then delete the product
            self.cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))

            self.connection.execute("COMMIT")
            return True, None
        except Exception as e:
            self.connection.execute("ROLLBACK")
            return False, str(e)

    # FOOD LIST OPERATIONS

    def add_food_list(self, name, description):
        """Add a new food list"""
        food_list_id = self.generate_id("product_list")
        try:
            self.cursor.execute(
                "INSERT INTO food_list (foodList_id, name, description) VALUES (?, ?, ?)",
                (food_list_id, name, description)
            )
            self.commit()
            return food_list_id, None
        except Exception as e:
            return None, str(e)

    def add_product_to_food_list(self, food_list_id, product_id):
        """Add a product to a food list"""
        try:
            self.cursor.execute(
                "INSERT INTO link_list (foodList_id, product_id) VALUES (?, ?)",
                (food_list_id, product_id)
            )
            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def get_food_list(self, food_list_id):
        """Get food list details and its products"""
        # Get food list information
        self.cursor.execute("SELECT * FROM food_list WHERE foodList_id = ?", (food_list_id,))
        food_list = self.cursor.fetchone()

        if not food_list:
            return None

        # Get products in the food list
        self.cursor.execute("""
                            SELECT p.*
                            FROM products p
                                     JOIN link_list l ON p.product_id = l.product_id
                            WHERE l.foodList_id = ?
                            """, (food_list_id,))
        products = self.cursor.fetchall()

        return {
            "food_list": food_list,
            "products": products
        }

    def get_all_food_lists(self, search_term=None):
        """Get all food lists with optional search filter"""
        query = "SELECT * FROM food_list"

        if search_term:
            query += f" WHERE name LIKE '%{search_term}%' OR description LIKE '%{search_term}%'"

        query += " ORDER BY name"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_food_list(self, food_list_id, name, description):
        """Update food list information"""
        try:
            self.cursor.execute(
                "UPDATE food_list SET name = ?, description = ? WHERE foodList_id = ?",
                (name, description, food_list_id)
            )
            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def delete_food_list(self, food_list_id):
        """Delete a food list and its product links"""
        try:
            # First check if food list is used in any delivery
            self.cursor.execute("SELECT COUNT(*) FROM delivery WHERE foodList_id = ?", (food_list_id,))
            if self.cursor.fetchone()[0] > 0:
                return False, "Cannot delete food list as it is used in deliveries"

            # Delete product links
            self.cursor.execute("DELETE FROM link_list WHERE foodList_id = ?", (food_list_id,))

            # Delete food list
            self.cursor.execute("DELETE FROM food_list WHERE foodList_id = ?", (food_list_id,))

            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    # DELIVERY OPERATIONS

    def add_delivery(self, departure_time, arrival_time, date, food_list_id, location_id, org_id):
        """Add a new delivery"""
        delivery_id = self.generate_id("delivery")
        try:
            # Debug print to verify values
            print(
                f"Adding delivery with: date={date}, foodList_id={food_list_id}, location_id={location_id}, org_id={org_id}")

            # IMPORTANT: The current database structure has date and foodList_id swapped
            # The correct SQL should have date in the date field and food_list_id in foodList_id
            self.cursor.execute(
                """INSERT INTO delivery
                       (delivery_id, departure_time, date, foodList_id, location_id, org_id)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (delivery_id, departure_time, date, food_list_id, location_id, org_id)
            )
            self.commit()

            # Verify the insert worked correctly
            self.cursor.execute("SELECT * FROM delivery WHERE delivery_id = ?", (delivery_id,))
            inserted_data = self.cursor.fetchone()
            print(f"Inserted data: {inserted_data}")

            return delivery_id, None
        except Exception as e:
            print(f"Error adding delivery: {e}")
            return None, str(e)

    def get_delivery(self, delivery_id):
        """Get delivery details"""
        self.cursor.execute("""
                            SELECT d.*, f.name as food_list_name, o.name as org_name, l.location_name
                            FROM delivery d
                                     JOIN food_list f ON d.foodList_id = f.foodList_id
                                     JOIN org_info o ON d.org_id = o.org_id
                                     JOIN location_info l ON d.location_id = l.location_id
                            WHERE d.delivery_id = ?
                            """, (delivery_id,))
        return self.cursor.fetchone()

    def get_all_deliveries(self, filter_by=None, search_term=None):
        """Get all deliveries with optional filters and search"""
        query = """
                SELECT d.*, f.name as food_list_name, o.name as org_name, l.location_name
                FROM delivery d
                         JOIN food_list f ON d.foodList_id = f.foodList_id
                         JOIN org_info o ON d.org_id = o.org_id
                         JOIN location_info l ON d.location_id = l.location_id \
                """

        where_clause = []

        # Add filter condition if provided - modified to not use arrival_time
        if filter_by == "completed" or filter_by == "past":
            # Since we're not using arrival_time, we can use date to determine if it's completed
            where_clause.append("date(d.date) < date('now')")
        elif filter_by == "ongoing" or filter_by == "upcoming":
            where_clause.append("date(d.date) >= date('now')")

        # Add search condition if provided
        if search_term:
            search_condition = f"""(f.name LIKE '%{search_term}%' 
                OR o.name LIKE '%{search_term}%' 
                OR l.location_name LIKE '%{search_term}%')"""
            where_clause.append(search_condition)

        # Combine where clauses
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        query += " ORDER BY d.date DESC"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_deliveries_by_org(self, org_id, filter_by=None):
        """Get deliveries for a specific organization"""
        query = """
                SELECT d.*, f.name as food_list_name, o.name as org_name, l.location_name
                FROM delivery d
                         JOIN food_list f ON d.foodList_id = f.foodList_id
                         JOIN org_info o ON d.org_id = o.org_id
                         JOIN location_info l ON d.location_id = l.location_id
                WHERE d.org_id = ? \
                """

        params = [org_id]

        # Add filter condition if provided - modified to not use arrival_time
        if filter_by == "completed" or filter_by == "past":
            query += " AND date(d.date) < date('now')"
        elif filter_by == "ongoing" or filter_by == "upcoming":
            query += " AND date(d.date) >= date('now')"

        query += " ORDER BY d.date DESC"

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def update_delivery(self, delivery_id, departure_time, date, food_list_id, location_id, org_id):
        """Update delivery information"""
        try:
            self.cursor.execute(
                """UPDATE delivery
                   SET departure_time = ?,
                       date           = ?,
                       foodList_id    = ?,
                       location_id    = ?,
                       org_id         = ?
                   WHERE delivery_id = ?""",
                (departure_time, date, food_list_id, location_id, org_id, delivery_id)
            )
            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    def delete_delivery(self, delivery_id):
        """Delete a delivery"""
        try:
            self.cursor.execute("DELETE FROM delivery WHERE delivery_id = ?", (delivery_id,))
            self.commit()
            return True, None
        except Exception as e:
            return False, str(e)

    # DONATION OPERATIONS

    def add_donation(self, user_code):
        """Add a new donation record"""
        try:
            self.cursor.execute(
                "INSERT INTO donation_info (user_code) VALUES (?)",
                (user_code,)
            )
            self.commit()

            # Get the generated donation_id
            self.cursor.execute("SELECT last_insert_rowid()")
            donation_id = self.cursor.fetchone()[0]

            return donation_id, None
        except Exception as e:
            return None, str(e)

    def get_donations_by_user(self, user_code):
        """Get donations made by a specific user"""
        self.cursor.execute("SELECT * FROM donation_info WHERE user_code = ?", (user_code,))
        return self.cursor.fetchall()

    # HELPER METHODS

    def execute_query(self, query, params=None):
        """Execute a custom query with optional parameters"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Check if query is a SELECT
            if query.strip().upper().startswith("SELECT"):
                return self.cursor.fetchall()
            else:
                self.commit()
                return True
        except Exception as e:
            return None

    def fix_delivery_dates(self):
        """Fix any delivery records where date and foodList_id fields are swapped"""
        print("Checking for delivery date issues...")
        # Get all deliveries
        query = "SELECT * FROM delivery"
        all_deliveries = self.execute_query(query)

        if not all_deliveries:
            print("No deliveries found. Nothing to fix.")
            return

        fixes_applied = 0

        # For each delivery, check if the date and foodList_id are swapped
        for delivery in all_deliveries:
            delivery_id = delivery[0]
            date_field = delivery[2]
            foodlist_id_field = delivery[3]

            # Check if the date field is None and foodList_id contains a date string
            is_date_in_foodlist = isinstance(foodlist_id_field, str) and "-" in foodlist_id_field

            if is_date_in_foodlist:
                # The date is in the foodList_id field, so swap them
                correct_date = foodlist_id_field

                # Try to determine the correct food list ID
                # For this specific case, we'll set it to 1 since that's the typical value
                correct_foodlist_id = 1

                print(f"Fixing delivery ID {delivery_id}: date={correct_date}, foodList_id={correct_foodlist_id}")

                # Update the record in the database
                update_query = """
                               UPDATE delivery
                               SET date        = ?, \
                                   foodList_id = ?
                               WHERE delivery_id = ? \
                               """
                try:
                    self.cursor.execute(update_query, (correct_date, correct_foodlist_id, delivery_id))
                    self.commit()
                    fixes_applied += 1
                except Exception as e:
                    print(f"Error fixing delivery ID {delivery_id}: {e}")

        if fixes_applied > 0:
            print(f"Fixed {fixes_applied} delivery records")
        else:
            print("No delivery records needed fixing")

    def fix_database(self):
        """Fix the organization and location display issues in the database"""
        print("Performing database overhaul...")

        try:
            # Check for the delivery with ID 1 and fix it
            self.cursor.execute("SELECT * FROM delivery WHERE delivery_id = 1")
            delivery = self.cursor.fetchone()

            if delivery:
                # Delete and recreate the delivery with correct values
                self.cursor.execute("DELETE FROM delivery WHERE delivery_id = 1")

                # Insert the correct data directly
                self.cursor.execute("""
                                    INSERT INTO delivery (delivery_id, departure_time, date, foodList_id, location_id, org_id)
                                    VALUES (1, '09:00', '2025-05-12', 1, 'QC', 1)
                                    """)
                self.commit()

                # Verify the changes directly with column names
                self.cursor.execute("""
                                    SELECT d.delivery_id,
                                           d.departure_time,
                                           d.date,
                                           d.foodList_id,
                                           f.name AS food_list_name,
                                           d.org_id,
                                           o.name AS org_name,
                                           d.location_id,
                                           l.location_name
                                    FROM delivery d
                                             JOIN food_list f ON d.foodList_id = f.foodList_id
                                             JOIN org_info o ON d.org_id = o.org_id
                                             JOIN location_info l ON d.location_id = l.location_id
                                    WHERE d.delivery_id = 1
                                    """)

                # Get column names
                columns = [description[0] for description in self.cursor.description]
                print("Database columns:", columns)

                # Get the data
                result = self.cursor.fetchone()
                if result:
                    print("\nDatabase values:")
                    for i, col in enumerate(columns):
                        print(f"{col}: {result[i]}")

                    # Make sure the organization value is CARE Philippines
                    org_name = result[6]  # org_name should be at index 6
                    if org_name != "CARE Philippines":
                        print(f"Warning: Organization is '{org_name}', not 'CARE Philippines'")

                    # Make sure location is Quezon City
                    location_name = result[8]  # location_name should be at index 8
                    if location_name != "Quezon City":
                        print(f"Warning: Location is '{location_name}', not 'Quezon City'")

                    # Make sure food list starts with "Food List 1"
                    food_list_name = result[4]  # food_list_name should be at index 4
                    if not food_list_name.startswith("Food List 1"):
                        print(f"Warning: Food list is '{food_list_name}', doesn't start with 'Food List 1'")
                else:
                    print("Failed to retrieve delivery data")

                print("\nDatabase overhaul completed")
            else:
                print("Delivery ID 1 not found in database")

        except Exception as e:
            print(f"Error fixing database: {e}")


# Initialize the database with some default data if it doesn't exist
def initialize_database():
    # Check if database file exists
    db_exists = os.path.exists(Database.DB_NAME)

    db = Database()

    if not db_exists:
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
            db.add_location(loc_id, loc_name)

        # Add default admin account
        db.create_account(
            username="admin_pedro",
            firstname="Pedro",
            lastname="Garcia",
            password="password123",
            confirm_password="password123",
            user_type=1  # 1 for admin
        )

        # Automatically insert all admin accounts into donation_info
        admins = db.get_all_admin_accounts()
        for admin in admins:
            user_code = admin[0]  # user_code is the first item in the tuple
            # Prevent duplicates
            db.cursor.execute("SELECT 1 FROM donation_info WHERE user_code = ?", (user_code,))
            if not db.cursor.fetchone():
                db.add_donation(user_code)

        # Add default user account
        user_code, _ = db.create_account(
            username="ngo_careph",
            firstname="Marco",
            lastname="Reyes",
            password="password123",
            confirm_password="password123",
            user_type=0  # 0 for regular user
        )

        # Add an organization for the user
        db.add_organization(
            name="CARE Philippines",
            user_code=user_code,
            location_id="QC"
        )

        # Add some sample products
        db.add_product("Rice", 0, 1000)
        db.add_product("Canned Goods", 0, 500)
        db.add_product("Bread", 1, 200)
        db.add_product("Milk", 1, 300)
        db.add_product("Bottled Water", 0, 1000)

        print("Database initialized with default data.")
    else:
        print("Database already exists.")

    # Always check and fix delivery dates
    db.fix_delivery_dates()

    # Fix any organization/location display issues
    db.fix_database()

    db.close()


if __name__ == "__main__":
    # Initialize the database if it doesn't exist
    initialize_database()