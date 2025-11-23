import os
import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Room, Booking

app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(Booking).delete()
        db.session.query(Room).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Create Admin User (if not exists from first_run_setup)
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@hotelhq.com',
                role='admin'
            )
            admin_user.set_password('admin')
            db.session.add(admin_user)

        # Create Staff Users
        staff1 = User(username='staff1', email='staff1@hotelhq.com', role='staff')
        staff1.set_password('staff123')
        staff2 = User(username='staff2', email='staff2@hotelhq.com', role='staff')
        staff2.set_password('staff123')
        db.session.add_all([staff1, staff2])

        # Create Customer Users
        customer1 = User(username='customer1', email='customer1@test.com', role='customer')
        customer1.set_password('customer123')
        customer2 = User(username='customer2', email='customer2@test.com', role='customer')
        customer2.set_password('customer123')
        db.session.add_all([customer1, customer2])

        db.session.commit()
        print("Users seeded.")

        # Create Rooms
        room_types = ['Single', 'Double', 'Suite', 'Deluxe']
        rooms = []
        for i in range(1, 21):
            room_type = random.choice(room_types)
            price_map = {'Single': 100, 'Double': 150, 'Suite': 250, 'Deluxe': 350}
            room = Room(
                room_number=str(100 + i),
                room_type=room_type,
                price_per_night=price_map[room_type] + random.randint(-20, 20),
                is_available=True,
                features=f"A comfortable {room_type.lower()} room with a great view."
            )
            rooms.append(room)
        db.session.add_all(rooms)
        db.session.commit()
        print(f"{len(rooms)} rooms seeded.")

        # Create Bookings
        all_rooms = Room.query.all()
        all_customers = User.query.filter_by(role='customer').all()
        bookings = []
        for _ in range(10):
            room = random.choice(all_rooms)
            customer = random.choice(all_customers)
            check_in_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
            check_out_date = check_in_date + timedelta(days=random.randint(1, 5))
            total_price = (check_out_date - check_in_date).days * room.price_per_night
            
            # Ensure no overlapping bookings for the same room
            existing_booking = Booking.query.filter(
                Booking.room_id == room.room_id,
                Booking.check_in_date < check_out_date,
                Booking.check_out_date > check_in_date
            ).first()

            if not existing_booking:
                booking = Booking(
                    user_id=customer.user_id,
                    room_id=room.room_id,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    total_price=total_price,
                    status='Confirmed',
                    payment_status='Pending'
                )
                bookings.append(booking)

        db.session.add_all(bookings)
        db.session.commit()
        print(f"{len(bookings)} bookings seeded.")
        print("Sample data seeding complete.")

if __name__ == '__main__':
    seed_data()
