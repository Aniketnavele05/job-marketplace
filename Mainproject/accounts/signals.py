from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TalentProfile, RecruiterProfile, CustomUser
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CustomUser)
def create_profile_user(sender, instance, created, **kwargs):
    try:
        if created:
            if instance.user_type == 'talent':
                TalentProfile.objects.create(user=instance)
                logger.info(f"TalentProfile created for {instance.username}")
            elif instance.user_type == 'recruiter':
                RecruiterProfile.objects.create(user=instance)
                logger.info(f"RecruiterProfile created for {instance.username}")
    except Exception as e:
        logger.error(f"Failed to create profile for {instance.username}: {str(e)}")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        if instance.user_type == 'talent' and hasattr(instance, 'talent_profile'):
            instance.talent_profile.save()
        elif instance.user_type == 'recruiter' and hasattr(instance, 'recruiter_profile'):
            instance.recruiter_profile.save()
    except Exception as e:
        logger.error(f"Failed to save profile for {instance.username}: {str(e)}")
