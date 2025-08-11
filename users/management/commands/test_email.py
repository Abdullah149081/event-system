from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Test email configuration by sending a test email"

    def add_arguments(self, parser):
        parser.add_argument(
            "--to", type=str, help="Email address to send test email to", required=True
        )

    def handle(self, *args, **options):
        recipient_email = options["to"]

        try:
            self.stdout.write("Testing email configuration...")
            self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
            self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
            self.stdout.write(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")

            subject = "Test Email from Django"
            message = "This is a test email to verify email configuration."
            from_email = settings.EMAIL_HOST_USER

            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[recipient_email],
                fail_silently=False,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Test email sent successfully to {recipient_email}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Failed to send test email: {str(e)}")
            )
