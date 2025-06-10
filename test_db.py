import mysql.connector
print("Testing database connection...")
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='hotel_management',
        user='root',
        password='gaurav123'
    )
    print("✓ Database connection successful!")
    
    cursor = connection.cursor()
    cursor.execute("DESCRIBE room")
    columns = cursor.fetchall()
    print(f"✓ Found {len(columns)} columns in room table:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    
    cursor.close()
    connection.close()
except Exception as e:
    print(f"✗ Error: {e}")
