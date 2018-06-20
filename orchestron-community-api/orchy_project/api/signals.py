from django.db.models.signals import post_save
from api.models import User

def create_random_password(sender, instance, **kwargs):
    created = kwargs.get('created')
    if created is True:
        if not instance.password:
            password = User.objects.make_random_password()
            # print(password)
            instance.set_password(password)
            instance.save()    

post_save.connect(create_random_password, sender=User)

