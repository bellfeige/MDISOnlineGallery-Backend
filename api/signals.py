from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, DesignerProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_designer:
            DesignerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_designer:
        instance.designer_profile.save()
