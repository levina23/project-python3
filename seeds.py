from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, User, Category, Event
# Define your database connection
DATABASE_URL = 'sqlite:///calendar_app.db'  # Use the same URL as in your models.py
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Define your seed data

# Sample Users
users_data = [
    {
        'username': 'user1',
        'email': 'user1@example.com',
        'password_hash': 'hashed_password1',
    },
    {
        'username': 'user2',
        'email': 'user2@example.com',
        'password_hash': 'hashed_password2',
    },
]

# Sample Categories
categories_data = [
    {
        'name': 'Meeting',
        'color': '#FF5733',
    },
    {
        'name': 'Birthday',
        'color': '#3366FF',
    },
]

# Sample Events
events_data = [
    {
        'title': 'Team Meeting',
        'description': 'Discuss project progress.',
        'start_datetime': datetime(2023, 9, 15, 10, 0),
        'end_datetime': datetime(2023, 9, 15, 12, 0),
        'location': 'Conference Room A',
        'user_id': 1,  # Assign this event to user with ID 1
        'category_id': 1,  # Assign this event to the "Meeting" category
    },
    {
        'title': 'Birthday Party',
        'description': 'Celebrate John\'s birthday.',
        'start_datetime': datetime(2023, 10, 5, 18, 0),
        'end_datetime': datetime(2023, 10, 5, 22, 0),
        'location': 'John\'s House',
        'user_id': 2,  # Assign this event to user with ID 2
        'category_id': 2,  # Assign this event to the "Birthday" category
    },
]

# Seed the database with the sample data

try:
    # Seed Users
    for user_data in users_data:
        user = User(**user_data)
        session.add(user)

    # Seed Categories
    for category_data in categories_data:
        category = Category(**category_data)
        session.add(category)

    # Seed Events
    for event_data in events_data:
        event = Event(**event_data)
        session.add(event)

    # Commit the changes
    session.commit()
    print("Seed data inserted successfully.")

except Exception as e:
    session.rollback()
    print(f"Error seeding data: {str(e)}")

finally:
    session.close()
