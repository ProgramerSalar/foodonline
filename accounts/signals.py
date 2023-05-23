from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import UserProfile , User 



@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender , instance , created , **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print('create profile successfully')

    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the userprofile if not exists
            UserProfile.objects.create(user=instance)
            print('Profile was not exist , but i created on')
        print('user is updated successfully')



@receiver(pre_save , sender=User)
def pre_save_profile_receiver(sender , instance , **kwargs):
    print(instance.username , 'this is user is being saved successfully')

# post.save.connect(post_save_create_profile_receiver , sender = User)