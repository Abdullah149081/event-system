from django.db import models
from django.contrib.auth.models import User
from .utils import optimize_image_for_web

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(
        upload_to="events_img", default="default.webp", blank=True
    )
    participants = models.ManyToManyField(User, related_name="rsvp_events", blank=True)
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_events",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.image:
            success = optimize_image_for_web(self.image)
            if success:
                super().save(update_fields=["image"])
