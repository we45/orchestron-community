from api.models import AccessToken
from rest_framework import authentication
from rest_framework import exceptions

class AccessKeyAuthentication(authentication.BaseAuthentication):
	def authenticate(self, request):
		access_key = request.META.get('HTTP_ACCESS_KEY', '')
		secret_key = request.META.get('HTTP_SECRET_KEY', '')
		if not access_key or not secret_key:
			return None
		try:
			access_key = AccessToken.objects.get(access_key=access_key, secret_key=secret_key)
			user = access_key.user
		except AccessToken.DoesNotExist:
			raise exceptions.AuthenticationFailed('Invalid user')
		return (user, None)