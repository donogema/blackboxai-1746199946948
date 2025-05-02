from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to perform additional actions when a user is created or updated.
    This can be extended to create related profiles or send notifications.
    """
    if created:
        # Add any initialization logic here
        pass
