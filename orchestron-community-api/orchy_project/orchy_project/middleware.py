from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from api.app_log import critical_debug_log
from django.conf import settings
from api.orchy_logger import log


class ExceptionMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		log.info('{0} has been accessed by {1}'.format(request.path,request.user))
		return self.get_response(request)	

	def process_exception(self, request, exception):
		log.error('Exception {0} has been raised'.format(exception))
		if isinstance(exception,ObjectDoesNotExist):
			return JsonResponse({'Error':'Object does not exists'},status=404)	

		