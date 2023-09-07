import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, User, Category, Event

# Define your database connection
DATABASE_URL = 'sqlite:///calendar_app.db'

# Create an SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    """Calendar/Event Planner CLI App"""

@cli.command()
def list_events():
    """List all events."""
    events = session.query(Event).all()
    if not events:
        click.echo("No events found.")
    else:
        click.echo("List of events:")
        for event in events:
            click.echo(f"- {event.title} ({event.start_datetime})")

@cli.command()
@click.option('--username', prompt='Enter your username', help='Your username')
@click.option('--email', prompt='Enter your email', help='Your email address')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Your password')
def create_user(username, email, password):
    """Create a new user."""
    user = User(username=username, email=email, password_hash=password)
    session.add(user)
    session.commit()
    click.echo("User created successfully.")

@cli.command()
@click.option('--title', prompt='Enter the event title', help='Event title')
@click.option('--description', prompt='Enter event description', help='Event description')
@click.option('--start-datetime', prompt='Enter start date and time (YYYY-MM-DD HH:MM)', help='Start date and time')
@click.option('--end-datetime', prompt='Enter end date and time (YYYY-MM-DD HH:MM)', help='End date and time')
@click.option('--location', prompt='Enter event location', help='Event location')
@click.option('--user-id', type=int, prompt='Enter user ID', help='User ID')
@click.option('--category-id', type=int, prompt='Enter category ID', help='Category ID')
def create_event(title, description, start_datetime, end_datetime, location, user_id, category_id):
    """Create a new event."""
    try:
        # Convert start_datetime and end_datetime to datetime objects
        start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M')
        end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M')

        # Create the event and add it to the database
        event = Event(
            title=title,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            user_id=user_id,
            category_id=category_id
        )
        session.add(event)
        session.commit()
        click.echo("Event created successfully.")
    except Exception as e:
        session.rollback()
        click.echo(f"Error creating event: {str(e)}")
    finally:
        session.close()

@cli.command()
def list_categories():
    """List all categories."""
    categories = session.query(Category).all()
    if not categories:
        click.echo("No categories found.")
    else:
        click.echo("List of categories:")
        for category in categories:
            click.echo(f"- {category.name} ({category.color})")

if __name__ == '__main__':
    cli()