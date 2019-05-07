from django.db.models.signals import post_save
from api.models import User, Webhook, Application, AccessToken
import binascii
import os

def create_random_password(sender, instance, **kwargs):
    created = kwargs.get('created')
    if created is True:
        if not instance.password:
            password = User.objects.make_random_password()
            instance.set_password(password)
            instance.save() 

def generate_access_tokens(sender, instance, **kwargs):
    created = kwargs.get('created')
    if created is True:  
        data_dict = {
            'access_key':binascii.hexlify(os.urandom(20)).decode(),
            'secret_key':binascii.hexlify(os.urandom(20)).decode(),
            'user':instance
        }    
        AccessToken.objects.create(**data_dict)             


def create_app_webhook(sender, instance, **kwargs):
    created = kwargs.get('created')
    if created is True:
        data_dict = {
        	'name':'{0}_Webhook'.format(instance.name),
        	'application':instance
        } 
        Webhook.objects.create(**data_dict)                

post_save.connect(create_random_password, sender=User)
post_save.connect(generate_access_tokens, sender=User)
post_save.connect(create_app_webhook, sender=Application)

