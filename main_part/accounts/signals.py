from django.db.models.signals import post_save
from .models import Account,UserProfile
from django.dispatch import receiver



@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()