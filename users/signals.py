from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Send activation email when a new user is created
    """
    if created and not instance.is_active:
        try:
            token = default_token_generator.make_token(instance)
            uid = urlsafe_base64_encode(force_bytes(instance.pk))

            activation_url = f"{settings.FRONTEND_URL}/users/activate/{uid}/{token}/"

            subject = "Activate Your Account - Event Management"
            message = f"""
Hi {instance.username},

Thank you for signing up for Event Management!

Please click the link below to activate your account:
{activation_url}

If you didn't create this account, please ignore this email.

Best regards,
The Event Management Team
            """.strip()

            recipient_list = [instance.email]

            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )

            print(f"Activation email sent successfully to {instance.email}")

        except Exception as e:
            print(f"Failed to send activation email to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()


def send_rsvp_confirmation_email(user, event):
    """Send RSVP confirmation email"""
    try:
        subject = f"RSVP Confirmation - {event.name}"
        message = f"""
Hi {user.username},

You have successfully RSVP'd to the event: {event.name}

Event Details:
- Title: {event.name}
- Date: {event.date}
- Location: {event.location}
- Description: {event.description}

We look forward to seeing you at the event!

Best regards,
Event Management Team
        """.strip()

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        print(f"RSVP confirmation email sent successfully to {user.email}")

    except Exception as e:
        print(f"Failed to send RSVP confirmation email to {user.email}: {str(e)}")
