from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from api.app_log import critical_debug_log
from django.conf import settings


class ExceptionMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.get_response(request)

	def process_exception(self, request, exception):
		if isinstance(exception,ObjectDoesNotExist):
			return JsonResponse({'Error':'Object does not exists'},status=404)
		# elif isinstance(exception,BaseException):
		# 	critical_debug_log(ip=request.get_host(), user=request.user.username, event=exception, status='failure')
		# 	return JsonResponse({'Status':'Error'},status=500)			

		