import os
import django
from faker import Faker
import random

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_system.settings")
django.setup()

from django.contrib.auth.models import User, Group
from events.models import Category, Event


def populate_event_system():
    fake = Faker()

    # Create Groups
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    organizer_group, _ = Group.objects.get_or_create(name="Organizer")
    participant_group, _ = Group.objects.get_or_create(name="Participant")

    print("Created user groups.")

    # Create Categories
    categories = [
        Category.objects.create(
            name=fake.word().capitalize(), description=fake.sentence()
        )
        for _ in range(5)
    ]
    print(f"Created {len(categories)} categories.")

    # Create Users (organizers and participants)
    organizers = []
    participants = []

    # Create organizers
    for i in range(3):
        username = f"organizer_{i+1}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=fake.unique.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
            )
            user.groups.add(organizer_group)
            organizers.append(user)

    # Create participants
    for i in range(15):
        username = f"participant_{i+1}"
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=fake.unique.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_active=True,
            )
            user.groups.add(participant_group)
            participants.append(user)

    print(f"Created {len(organizers)} organizers and {len(participants)} participants.")

    # Create Events
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories),
            created_by=random.choice(organizers) if organizers else None,
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Assign participants to events using ManyToMany relationship
    for event in events:
        # Randomly select participants for each event
        event_participants = random.sample(
            participants, random.randint(3, min(8, len(participants)))
        )

        for participant in event_participants:
            # Add participant to event using the simplified ManyToMany relationship
            event.participants.add(participant)

    print("Assigned participants to events.")
    print("Event system database populated successfully!")


populate_event_system()
