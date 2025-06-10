#!/usr/bin/env python3
"""
Script to update the room table schema with missing columns
"""

import mysql.connector
from mysql.connector import Error
import sys

def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='hotel_management',
            user='root',
            password='gaurav123'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def update_room_schema():
    """Update room table schema to add missing columns"""
    connection = create_connection()
    if not connection:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Get current columns
        cursor.execute("DESCRIBE room")
        columns = [col[0] for col in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
        updates_made = []
        
        # Add Room_type column if missing
        if 'Room_type' not in columns:
            try:
                cursor.execute("ALTER TABLE room ADD COLUMN Room_type VARCHAR(50) DEFAULT 'Standard'")
                updates_made.append('Room_type')
                print("Added Room_type column")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"Error adding Room_type: {e}")
                else:
                    print("Room_type column already exists")
        
        # Add description column if missing
        if 'description' not in columns:
            try:
                cursor.execute("ALTER TABLE room ADD COLUMN description TEXT")
                updates_made.append('description')
                print("Added description column")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"Error adding description: {e}")
                else:
                    print("description column already exists")
        
        # Add room_image column if missing
        if 'room_image' not in columns:
            try:
                cursor.execute("ALTER TABLE room ADD COLUMN room_image VARCHAR(255)")
                updates_made.append('room_image')
                print("Added room_image column")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"Error adding room_image: {e}")
                else:
                    print("room_image column already exists")
        
        # Add Room_Price column if missing
        if 'Room_Price' not in columns:
            try:
                cursor.execute("ALTER TABLE room ADD COLUMN Room_Price DECIMAL(10,2) NOT NULL DEFAULT 0.00")
                updates_made.append('Room_Price')
                print("Added Room_Price column")
            except Error as e:
                if "Duplicate column name" not in str(e):
                    print(f"Error adding Room_Price: {e}")
                else:
                    print("Room_Price column already exists")
        
        # Update existing rooms without Room_type
        if 'Room_type' in updates_made or 'Room_type' in columns:
            cursor.execute("UPDATE room SET Room_type = 'Standard' WHERE Room_type IS NULL OR Room_type = ''")
            print("Updated existing rooms with default Room_type")
        
        connection.commit()
        
        print(f"\nSchema update completed successfully!")
        if updates_made:
            print(f"Added columns: {', '.join(updates_made)}")
        else:
            print("No new columns needed - schema is up to date")
        
        # Show final schema
        cursor.execute("DESCRIBE room")
        final_columns = cursor.fetchall()
        print("\nFinal room table schema:")
        for col in final_columns:
            print(f"  {col[0]} - {col[1]} - {col[2]} - {col[3]} - {col[4]} - {col[5]}")
        
        return True
        
    except Error as e:
        connection.rollback()
        print(f"Error updating schema: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    print("Updating room table schema...")
    success = update_room_schema()
    if success:
        print("\n✓ Schema update completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Schema update failed!")
        sys.exit(1)
