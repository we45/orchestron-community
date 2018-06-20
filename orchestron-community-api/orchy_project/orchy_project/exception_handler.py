from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

def custom_exception_handler(exc, context):
	response = exception_handler(exc, context)
	return response