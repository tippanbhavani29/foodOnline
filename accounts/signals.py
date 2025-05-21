 

 
#post_save.connect(post_save_create_profile_reciever,sender=User)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile  # Import your custom model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, User

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)  # Simpler & safer

# @receiver(post_save, sender=User)
# def post_save_create_profile_receiver(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#     else:
#         try:
#             profile = UserProfile.objects.get(user=instance)
#             profile.save()
#         except :
#             UserProfile.objects.create(user=instance)













                        