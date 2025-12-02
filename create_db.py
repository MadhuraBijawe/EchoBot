import MySQLdb

try:
    db = MySQLdb.connect(host="localhost", user="root", passwd="")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS support_db")
    print("Database 'support_db' created or already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
    print("Please ensure MySQL is running and credentials are correct.")
