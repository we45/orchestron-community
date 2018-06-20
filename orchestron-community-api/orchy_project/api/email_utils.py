import sys
# from django.contrib.sites.models import Site
from django.conf import settings
from django.core.mail import send_mail,EmailMultiAlternatives,get_connection
from django.utils.http import int_to_base36, urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from api.ciphertext_manager import EmailCipher
from api.app_log import *


def test_email_connection(host,port,username,password,certs,from_email):
    try:
        if certs == 'SSL':
            USE_TLS = None
            USE_SSL = True
        else:
            USE_TLS = True
            USE_SSL = None
        connection = get_connection(host=host,port=port,username=username,password=password,
            use_tls=USE_TLS, fail_silently=False, use_ssl=USE_SSL, timeout=None)
        connection.open()
        email = EmailMultiAlternatives("Welcome to Orchestron", 'This is a connection test email', from_email, [settings.DEFAULT_USER_EMAIL],connection=connection)
        email.send()
        connection.close()
    except BaseException as e:
        return False
    else:
        return True


def send_email_to_users(user, domain_override, email_template_name,use_https, token_generator):
    """
    input description: 
    parameter one - created user info
    parameter two - the domain name form where the email has to be sent
    parameter three - the path of the email template that needs to be rendered to send mail
    parameter four - protocol used to send mail (http or https) 
    parameter five - built in method to generate a unique token for the user
    input type: 
    parameter one - unicode
    parameter two - string
    parameter three - html
    parameter four - built in methods
    parameter five - built in methods
    action preformed: sends email on user creation
    template used: NA
    """
    try:
        a = AESCipher()
        email_obj = EmailConfiguration.objects.last()
        EMAIL_HOST = a.decrypt(email_obj.email_host)
        EMAIL_PORT = a.decrypt(email_obj.email_port)
        EMAIL_HOST_USER = a.decrypt(email_obj.email_host_user)
        EMAIL_HOST_PASSWORD = a.decrypt(email_obj.email_host_password)
        from_email = a.decrypt(email_obj.email_from_email)
        display_email = a.decrypt(email_obj.email_display_name)
        email_certs = a.decrypt(email_obj.email_certs)
        if email_certs == 'SSL':
            USE_TLS = None
            USE_SSL = True
        else:
            USE_TLS = True
            USE_SSL = None
        connection = get_connection(host=EMAIL_HOST,port=EMAIL_PORT,username=EMAIL_HOST_USER,password=EMAIL_HOST_PASSWORD,
            use_tls=USE_TLS, fail_silently=False, use_ssl=USE_SSL, timeout=None)
        connection.open()
        from_full_email = '{0} <{1}>'.format(display_email,from_email)
        if not user.email:
            raise ValueError('Email address is required to send an email')
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'name':user.username,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(str(user.id)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            'auth_token':user.auth_token
        }
        email = EmailMultiAlternatives("Welcome to Orchestron", '', from_full_email, [user.email],connection=connection)
        email.attach_alternative(t.render(c), "text/html")
        email.send()
        info_debug_log(user=user,event='Send email to users',status='success')
        connection.close()
    except:
        from_email = 'Orchestron'
        
        if not user.email:
            error_debug_log(user=user,event='Email address is not provided',status='failure')
            raise ValueError('Email address is required to send an email')
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'name':user.username,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(str(user.id)),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            'auth_token':user.auth_token
        }
        email = EmailMultiAlternatives("Welcome to Orchestron", '', from_email, [user.email])
        email.attach_alternative(t.render(c), "text/html")
        email.send()
        info_debug_log(user=user,event='Send email to users',status='success')