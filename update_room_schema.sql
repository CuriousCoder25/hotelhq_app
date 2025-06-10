-- SQL script to update room table for enhanced room management

-- Add missing columns to room table if they don't exist
ALTER TABLE room 
ADD COLUMN description TEXT,
ADD COLUMN room_image VARCHAR(255),
ADD COLUMN Room_type VARCHAR(50) DEFAULT 'Standard';

-- Make sure Room_Price column exists (if not already added)
ALTER TABLE room ADD COLUMN Room_Price DECIMAL(10,2) NOT NULL DEFAULT 0.00;

-- Update any existing rooms without a Room_type to have a default
UPDATE room SET Room_type = 'Standard' WHERE Room_type IS NULL OR Room_type = '';

-- Sample data for testing (optional)
-- INSERT INTO room (room_number, Room_type, Room_Price, Status, description) VALUES
-- ('101', 'Single', 89.99, 'Available', 'Cozy single room with city view'),
-- ('102', 'Double', 129.99, 'Available', 'Spacious double room with queen bed'),
-- ('201', 'Suite', 249.99, 'Available', 'Luxury suite with separate living area'),
-- ('202', 'Deluxe', 189.99, 'Maintenance', 'Deluxe room with premium amenities');
