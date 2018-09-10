from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from rest_framework.response import Response

class OrchyPagination(LimitOffsetPagination):
	sev_context = {}

	def get_paginated_response(self, data):
		return Response(OrderedDict([
			('count', self.count),
			('next', self.get_next_link()),
			('previous', self.get_previous_link()),
			('results', data),
			('severity',self.sev_context)
		]))