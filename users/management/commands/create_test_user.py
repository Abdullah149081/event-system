from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create a test user to test email activation"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Username for the test user",
            default="testuser123",
        )
        parser.add_argument(
            "--email",
            type=str,
            help="Email for the test user",
            default="test@example.com",
        )

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"User {username} already exists. Deleting...")
            User.objects.filter(username=username).delete()

        self.stdout.write(f"Creating test user: {username} with email: {email}")

        # Create user (this should trigger the signal)
        user = User.objects.create_user(
            username=username,
            email=email,
            password="testpassword123",
            is_active=False,  # This should trigger the email
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Test user created: {user.username} (Active: {user.is_active})"
            )
        )
