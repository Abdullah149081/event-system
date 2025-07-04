import os
import django
from faker import Faker
import random
# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_system.settings")
django.setup()

from events.models import (
    Category,
    Event,
    Participant,
)  # adjust if app name is different


def populate_event_system():
    fake = Faker()

    # Create Categories
    categories = [
        Category.objects.create(
            name=fake.word().capitalize(), description=fake.sentence()
        )
        for _ in range(5)
    ]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = [
        Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories),
        )
        for _ in range(10)
    ]
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = [
        Participant.objects.create(name=fake.name(), email=fake.unique.email())
        for _ in range(20)
    ]
    print(f"Created {len(participants)} participants.")

    # Assign Participants to Events
    for event in events:
        event.participants.set(random.sample(participants, random.randint(3, 10)))

    print("Assigned participants to events.")
    print("Event system database populated successfully!")


populate_event_system()
