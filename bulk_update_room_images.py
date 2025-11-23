import os
import shutil
from app import create_app, db
from app.models import Room

# Source folder with images
SOURCE_FOLDER = r"C:\Users\The Climber\Desktop\gemini-images"
# Destination folder (uploads)
DEST_FOLDER = r"C:\Users\The Climber\Desktop\new hh 2\hotelhq\app\static\uploads"

def bulk_update_images():
    """Copy images from source folder and assign them to rooms"""
    app = create_app()
    
    with app.app_context():
        # Get all image files from source folder
        if not os.path.exists(SOURCE_FOLDER):
            print(f"Error: Source folder '{SOURCE_FOLDER}' does not exist!")
            return
        
        # Create destination folder if it doesn't exist
        if not os.path.exists(DEST_FOLDER):
            os.makedirs(DEST_FOLDER)
            print(f"Created uploads folder: {DEST_FOLDER}")
        
        # Get all image files
        image_files = [f for f in os.listdir(SOURCE_FOLDER) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        
        if not image_files:
            print(f"No image files found in {SOURCE_FOLDER}")
            return
        
        print(f"Found {len(image_files)} images in source folder")
        
        # Get all rooms
        rooms = Room.query.all()
        print(f"Found {len(rooms)} rooms in database")
        
        if not rooms:
            print("No rooms found in database!")
            return
        
        # Update rooms with images
        updated_count = 0
        for i, room in enumerate(rooms):
            # Cycle through images if more rooms than images
            image_index = i % len(image_files)
            source_image = image_files[image_index]
            
            # Get file extension
            _, ext = os.path.splitext(source_image)
            
            # Create new filename: room_<room_number><extension>
            new_filename = f"room_{room.room_number}{ext}"
            
            # Copy image to uploads folder
            source_path = os.path.join(SOURCE_FOLDER, source_image)
            dest_path = os.path.join(DEST_FOLDER, new_filename)
            
            try:
                shutil.copy2(source_path, dest_path)
                
                # Update room's image_url
                room.image_url = new_filename
                updated_count += 1
                
                print(f"✓ Room {room.room_number} ({room.room_type}): {source_image} -> {new_filename}")
            
            except Exception as e:
                print(f"✗ Error updating room {room.room_number}: {e}")
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✓ Successfully updated {updated_count} rooms with images!")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error saving to database: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("Bulk Room Image Updater")
    print("=" * 60)
    print(f"Source: {SOURCE_FOLDER}")
    print(f"Destination: {DEST_FOLDER}")
    print("=" * 60)
    
    bulk_update_images()
    
    print("=" * 60)
    print("Done!")
