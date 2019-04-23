from collections import Counter
from django.shortcuts import get_object_or_404
from django.db.models import Count, Max, Min, Value as V, Q, F
from django.db.models.functions import Concat
from rest_framework import serializers, viewsets,status
from rest_framework.response import Response
from api.exceptions import QueryMisMatchError
from api.db_funcs import GroupConcat, Aging, ExtractMonth, ExtractYear, ExtractDate
from api.stored_procedures import ReportProcedures
from api.models import Organization,Project,Application,Vulnerability,Engagement,Scan
from rest_framework.authentication import TokenAuthentication
from api.utils import get_severity_by_name
from api.serializers import QueryParamSerializer, BasePostParamSerializer, \
	RaiseJIRATicketSerializer, OpenVulSerializer, ClosedVulSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from api.orl import get_open_vul_info_from_api
from django.core.serializers import serialize
import json
import math
from api.tasks import webhook_upload, webhook_process_json, raise_jira_ticket
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.pagination import OrchyPagination
from django.conf import settings


class OpenVulnerabilityStatView(viewsets.ViewSet):
    def get_open_vul_query(self, kwargs={}, exclude_kwargs={}):
        new_kwargs = kwargs
        new_kwargs['is_false_positive'] = kwargs.get('is_false_positive',False)
        open_vuls = Vulnerability.objects.filter(is_remediated=False).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .exclude(cwe__in=settings.JANATHA_CLASS)\
            .values('cwe')\
            .distinct()\
            .order_by('cwe')
        janatha_vuls = Vulnerability.objects.filter(cwe__in=settings.JANATHA_CLASS,is_remediated=False).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .values('cwe')\
            .distinct()\
            .order_by('cwe') 
        return open_vuls | janatha_vuls          

    def vuls(self, kwargs={}, exclude_kwargs={}):
        ReportProcedures.set_max_value()
        raw_vuls = self.get_open_vul_query(kwargs, exclude_kwargs)     
        open_vuls = raw_vuls.annotate(tools=GroupConcat('tool',distinct=True),\
                count=Count('name',distinct=True),\
                apps=GroupConcat('scan__application__name',distinct=True),\
                common_name=GroupConcat('common_name',distinct=True),\
                open_for=Aging('created_on'),\
                names=GroupConcat(Concat('name',V('###'),'scan__application__name',V('###'),'jira_id',V('###'),'jira_issue_status'),distinct=True))         
        return open_vuls.values('tools','severity','apps','common_name','open_for','names','cwe','count').order_by('-severity')

    def avg_ageing(self, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_query(kwargs, exclude_kwargs)
        open_vuls = raw_vuls.annotate(open_for=Aging('created_on')) 
        avg_ageing_val = 0  
        if open_vuls:
            all_ageing_count = [v.get('open_for') for v in open_vuls]
            if all_ageing_count:
                avg_ageing_val = math.ceil(sum(all_ageing_count)/len(all_ageing_count))
        return avg_ageing_val       

    def count(self, kwargs={}, exclude_kwargs={}):
        vuls = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('severity',flat=True)
        return sum(dict(Counter(vuls)).values())

    def max_min_cvss(self, kwargs={}, exclude_kwargs={}):
        cvss = self.get_open_vul_query(kwargs, exclude_kwargs).aggregate(max_cvss=Max('cvss'),min_cvss=Min('cvss'))
        return cvss

    def risks(self, kwargs={}, exclude_kwargs={}):
        cwes = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('scan__application__org','cwe')
        risk_list = []
        for org,cwe in cwes:
            if org.orl_config_exists():
                vul_info = get_open_vul_info_from_api(cwe,org)
                risk_list.extend(vul_info.get('risk',[]))
        return list(set(risk_list))

    def severity_count(self, kwargs={}, exclude_kwargs={}):
        sevs = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('severity',flat=True)
        return dict(Counter(sevs))

    def cwe_severity_count(self, kwargs={}, exclude_kwargs={}):
        cwes = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('cwe','severity')
        return self.process_list(cwes)

    def tool_severity_count(self, kwargs={}, exclude_kwargs={}):
        tools = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('tool','severity')
        return self.process_list(tools)     

    def owasp_severity_count(self, kwargs={}, exclude_kwargs={}):
        owasps = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('owasp','severity')
        return self.process_list(owasps)

    def scan_severity_count(self, kwargs={}, exclude_kwargs={}):
        scans = self.get_open_vul_query(kwargs, exclude_kwargs)\
        .values_list('scan__short_name','severity')
        return self.process_list(scans)     

    def application_severity_count(self, kwargs={}, exclude_kwargs={}):
        applications = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('scan__application__id','scan__application__name','severity')
        return self.process_apps(applications)

    def months_count(self, kwargs={}, exclude_kwargs={}):
        months = self.get_open_vul_query(kwargs, exclude_kwargs)\
        .annotate(m=ExtractMonth('created_on'),y=ExtractYear('created_on'),month=Concat(V('01'),V('-'),'m',V('-'),'y'))\
        .values_list('month',flat=True)
        return dict(Counter(months))

    def month_severity_count(self, kwargs={}, exclude_kwargs={}):
        months = self.get_open_vul_query(kwargs, exclude_kwargs)\
        .annotate(m=ExtractMonth('created_on'),y=ExtractYear('created_on'),\
            month=Concat(V('01'),V('-'),'m',V('-'),'y'),severity=F('severity'))\
        .values_list('month','severity')
        return self.process_list(months)    

    def years_count(self, kwargs={}, exclude_kwargs={}):
        years = self.get_open_vul_query(kwargs, exclude_kwargs)\
        .annotate(year=ExtractYear('created_on'))\
        .values_list('year',flat=True)
        return dict(Counter(years))

    def year_severity_count(self, kwargs={}, exclude_kwargs={}):
        years = self.get_open_vul_query(kwargs, exclude_kwargs)\
        .annotate(year=ExtractYear('created_on'),severity=F('severity'))\
        .values_list('year','severity')
        return self.process_list(years) 

    def grade(self, kwargs={}, exclude_kwargs={}):
        cvss_dread_list = self.get_open_vul_query(kwargs, exclude_kwargs).values_list('cvss','dread')
        value = max([(y[0] or 0 + y[1] or 0) / 2 for y in cvss_dread_list] or [0])
        if value >= 1 and value <= 29:
            return 'F'
        elif value >= 30 and value <= 44:
            return 'E'
        elif value >= 45 and value <= 59:
            return 'D'
        elif value >= 60 and value <= 74:
            return 'C'
        elif value >= 75 and value <= 89:
            return 'B'
        elif value >= 90 and value <= 100:
            return 'A'
        else:
            return 'No Data'                            

    # def aging_count(self, kwargs={}, exclude_kwargs={}):
    #     aging_list = self.get_open_vul_query(kwargs, exclude_kwargs)\
    #     .annotate(open_for=Aging('created_on'))\
    #     .values_list('open_for',flat=True)
    #     days = dict(Counter(aging_list))
    #     days_list = []
    #     for day, count in days.items():
    #         if day <= 5:
    #             days_list.append(('0-5 days',count))
    #         elif day > 5 and day <= 10: 
    #             days_list.append(('6-10 days',count))
    #         elif day > 10 and day <= 20: 
    #             days_list.append(('11-20 days',count))
    #         elif day > 20 and day <= 40: 
    #             days_list.append(('21-40 days',count))
    #         elif day > 40 and day <= 80: 
    #             days_list.append(('41-80 days',count))
    #         elif day > 80 and day <= 100: 
    #             days_list.append(('81-100 days',count))
    #         elif day > 100:
    #             days_list.append(('More than 100 days',count))
    #     return days_list

    def aging_count(self, kwargs={}, exclude_kwargs={}):
        aging_list = self.get_open_vul_query(kwargs, exclude_kwargs)\
        .annotate(open_for=Aging('created_on'))\
        .values_list('open_for','severity')
        days = dict(Counter(aging_list))
        days_dict = {
			1:{'0-5 days':{0:0,1:0,2:0,3:0}},
			2:{'6-10 days':{0:0,1:0,2:0,3:0}},
			3:{'11-20 days':{0:0,1:0,2:0,3:0}},
			4:{'21-40 days':{0:0,1:0,2:0,3:0}},
			5:{'41-80 days':{0:0,1:0,2:0,3:0}},
			6:{'81-100 days':{0:0,1:0,2:0,3:0}},
			7:{'More than 100 days':{0:0,1:0,2:0,3:0}},
		}
        for day, severity in aging_list:
            if day <= 5:
              days_dict[1]['0-5 days'][severity] = days_dict[1]['0-5 days'][severity] + 1
            elif day > 5 and day <= 10:
              days_dict[2]['6-10 days'][severity] = days_dict[2]['6-10 days'][severity] + 1
            elif day > 10 and day <= 20:
              days_dict[3]['11-20 days'][severity] = days_dict[3]['11-20 days'][severity] + 1
            elif day > 20 and day <= 40:
              days_dict[4]['21-40 days'][severity] = days_dict[4]['21-40 days'][severity] + 1
            elif day > 40 and day <= 80:
              days_dict[5]['41-80 days'][severity] = days_dict[5]['41-80 days'][severity] + 1
            elif day > 80 and day <= 100:
              days_dict[6]['81-100 days'][severity] = days_dict[6]['81-100 days'][severity] + 1
            elif day > 100:
                days_dict[7]['More than 100 days'][severity] = days_dict[7]['More than 100 days'][severity] + 1
        return days_dict

    def heatmap(self, kwargs={}):
        scans = Scan.objects.filter(**kwargs).annotate(date=ExtractDate('created_on')).values('date').annotate(count=Count('id')).order_by('date').values_list('date','count')                    
        return scans

    def process_list(self, data_list):
        d = {}
        for c,i in data_list:
            if c not in d:
                d[c] = {0:0,1:0,2:0,3:0}
            d[c][i] = d[c][i] + 1               
        return d

    def process_severites(self, normal, janatha):
        dd = {1:0,2:0,3:0,0:0}
        for d in (normal, janatha):
            for key, value in d.items():
                dd[key] = dd[key] + value
        return dd       

    def process_apps(self, data_list):
        d = {}
        for id,app,sev in data_list:
            if app not in d:
                d[app] = {}
                d[app]['id'] = id
                d[app]['sev'] = {0:0,1:0,2:0,3:0}
            d[app]['sev'][sev] = d[app]['sev'][sev] + 1             
        return d        


class ClosedVulnerabilityStatView(viewsets.ViewSet):
    def get_closed_vul_query(self, kwargs, exclude_kwargs):
        new_kwargs = kwargs
        new_kwargs['is_false_positive'] = kwargs.get('is_false_positive',False)
        closed_vuls = Vulnerability.objects.filter(is_remediated=True).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .exclude(cwe__in=settings.JANATHA_CLASS)\
            .values('cwe')\
            .distinct()\
            .order_by('cwe')
        janatha_vuls = Vulnerability.objects.filter(cwe__in=settings.JANATHA_CLASS,is_remediated=True).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .values('cwe')\
            .distinct()\
            .order_by('cwe') 
        return closed_vuls | janatha_vuls          

    def vuls(self, kwargs={}, exclude_kwargs={}):
        ReportProcedures.set_max_value()
        raw_vuls = self.get_closed_vul_query(kwargs, exclude_kwargs)         
        closed_vuls = raw_vuls.annotate(tools=GroupConcat('tool',distinct=True),\
                count=Count('name',distinct=True),\
                apps=GroupConcat('scan__application__name',distinct=True),\
                common_name=GroupConcat('common_name',distinct=True),\
                created_on=Min('created_on'),\
                closed_on=Min('vulnerabilityremediation__remediated_on'),\
                names=GroupConcat(Concat('name',V('###'),'scan__application__name',V('###'),'jira_id',V('###'),'jira_issue_status'),distinct=True))         
        return closed_vuls.values('created_on','closed_on','tools','severity','apps','common_name','names','cwe','count').order_by('-severity')

    def count(self, kwargs={}, exclude_kwargs={}):
        vuls = self.get_closed_vul_query(kwargs, exclude_kwargs).values_list('severity',flat=True)
        return sum(dict(Counter(vuls)).values())

    def severity_count(self, kwargs={}, exclude_kwargs={}):
        sevs = self.get_closed_vul_query(kwargs, exclude_kwargs).values_list('severity',flat=True)
        return dict(Counter(sevs))


class BaseAnalyticsView(OrchyPagination,viewsets.ViewSet):
	"""
	Analytics Base View for Organization, Project, Application and Engagement
	"""

	def get_context(self,data,kwargs):
		"""
		Parameters
			cwe : int (max length = 4)

			severity : string (allowed options "info","low","medium","high")

			owasp : string 

			tool : string (allowed options "ZAP","Burp")

			start_date : date 

			stop_date : date 

			jira_sync : boolean 

			false : boolean 
		"""
		serializer = QueryParamSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		false_positive = serializer.validated_data.get('false',False)
		true_positive = serializer.validated_data.get('true',False)
		cwe = serializer.validated_data.get('cwe',False)
		severity = serializer.validated_data.get('severity',False)
		owasp = serializer.validated_data.get('owasp',False)
		name = serializer.validated_data.get('name',False)
		tool = serializer.validated_data.get('tool',False)
		jira_sync = serializer.validated_data.get('jira_sync',False)
		start_date = serializer.validated_data.get('start_date',False)
		stop_date = serializer.validated_data.get('stop_date',datetime.today().date())
		if cwe:
			kwargs['cwe'] = cwe
		if tool:
			kwargs['tool'] = tool
		if owasp:
			kwargs['owasp'] = owasp
		if start_date:
			kwargs['created_on__date__range'] = [start_date,stop_date]
		if jira_sync:
			kwargs['jira_id__isnull'] = False
		if name:
			kwargs['name'] = name			
		if severity:
			kwargs['severity'] = get_severity_by_name(severity)	
		if false_positive:
			kwargs['is_false_positive'] = True	
		if true_positive:
			kwargs['is_false_positive'] = False	
		o = OpenVulnerabilityStatView()				
		context = o.vuls(kwargs=kwargs)
		sev_context = o.severity_count(kwargs=kwargs)
		return context,sev_context

	def get_closed_vul_context(self,data,kwargs):
		"""
		Parameters
			cwe : int (max length = 4)

			severity : string (allowed options "info","low","medium","high")

			owasp : string 

			tool : string (allowed options "ZAP","Burp")

			start_date : date 

			stop_date : date 

			jira_sync : boolean 

			false : boolean 
		"""
		serializer = QueryParamSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		false_positive = serializer.validated_data.get('false',False)
		true_positive = serializer.validated_data.get('true',False)
		cwe = serializer.validated_data.get('cwe',False)
		severity = serializer.validated_data.get('severity',False)
		owasp = serializer.validated_data.get('owasp',False)
		tool = serializer.validated_data.get('tool',False)
		jira_sync = serializer.validated_data.get('jira_sync',False)
		start_date = serializer.validated_data.get('start_date',False)
		stop_date = serializer.validated_data.get('stop_date',datetime.today().date())
		if cwe:
			kwargs['cwe'] = cwe
		if tool:
			kwargs['tool'] = tool
		if owasp:
			kwargs['owasp'] = owasp
		if start_date:
			kwargs['created_on__date__range'] = [start_date,stop_date]
		if jira_sync:
			kwargs['jira_id__isnull'] = False
		if severity:
			kwargs['severity'] = get_severity_by_name(severity)	
		if false_positive:
			kwargs['is_false_positive'] = True	
		if true_positive:
			kwargs['is_false_positive'] = False	
		c = ClosedVulnerabilityStatView()		
		context = c.vuls(kwargs=kwargs)
		sev_context = c.severity_count(kwargs=kwargs)
		return context,sev_context


class OrganizationAnalyticsView(BaseAnalyticsView):
	"""
	Analytics view for Organization
	"""

	def get_queryset(self,user):
		"""
		Filter Organization's by user
		"""
		return Organization.objects.all()

	def retrieve_open(self, request, pk=None):
		"""
		Fetch open vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		apps = Application.objects.all()
		kwargs = {
			'scan__application__org':obj,
			'scan__application__in':apps
		}
		context, sev_context = self.get_context(self.request.query_params,kwargs)
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = OpenVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = OpenVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)

	def retrieve_closed(self, request, pk=None):
		"""
		Fetch closed vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		apps = Application.objects.all()
		kwargs = {
			'scan__application__org':obj,
			'scan__application__in':apps
		}
		context, sev_context = self.get_closed_vul_context(self.request.query_params,kwargs)	
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = ClosedVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = ClosedVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)					        


class ProjectAnalyticsView(BaseAnalyticsView):
	"""
	Analytics view for Project
	"""

	def get_queryset(self,user):
		"""
		Filter Project's by user
		"""
		return Project.objects.all()
		
	def retrieve_open(self, request, pk=None):
		"""
		Fetch open vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		apps = Application.objects.all()
		kwargs = {
			'scan__application__project':obj,
			'scan__application__in':apps
		}
		context, sev_context = self.get_context(self.request.query_params,kwargs)	
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = OpenVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = OpenVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)

	def retrieve_closed(self, request, pk=None):
		"""
		Fetch closed vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		apps = Application.objects.all()
		kwargs = {
			'scan__application__project':obj,
			'scan__application__in':apps
		}
		context, sev_context = self.get_closed_vul_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = ClosedVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = ClosedVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)			


class ApplicationAnalyticsView(BaseAnalyticsView):
	"""
	Analytics view for Application
	"""

	def get_queryset(self,user):
		"""
		Filter Applications's by user
		"""
		return Application.objects.all()
		
	def retrieve_open(self, request, pk=None):
		"""
		Fetch open vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__application':obj
		}
		context, sev_context = self.get_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = OpenVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = OpenVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)

	def retrieve_closed(self, request, pk=None):
		"""
		Fetch closed vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__application':obj
		}
		context, sev_context = self.get_closed_vul_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = ClosedVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = ClosedVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)	

	def update_open(self, request, pk=None):
		"""
		Update open vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		serializer = QueryParamSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		name = serializer.validated_data.get('name',False)
		owasp = serializer.validated_data.get('owasp',False)
		cwe = serializer.validated_data.get('cwe',False)
		severity = serializer.validated_data.get('severity',False)
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__application':obj
		}
		context, sev_context = self.get_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		return Response(context)

	def mark_open_vul_false_positive(self, request, pk=None):
		"""
		Mark open vulnerabilities as false positive by query params

		Parameters:
			pk : integer
		"""
		serializer = BasePostParamSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		name = serializer.validated_data.get('name')
		cwe = serializer.validated_data.get('cwe')
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__application':obj,
			'name':name,
			'cwe':cwe,
			'is_false_positive':False
		}
		vuls = OpenVulnerabilityStatView().get_open_vul_query(kwargs=kwargs)		
		if not vuls.exists():
			raise QueryMisMatchError
		vuls.update(is_false_positive=True)
		return Response({'message':'Vulnerabilities are been marked as false positive'},status=status.HTTP_200_OK)

	def mark_open_vul_true_positive(self, request, pk=None):
		"""
		Mark open vulnerabilities as false positive by query params

		Parameters:
			pk : integer
		"""
		serializer = BasePostParamSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		name = serializer.validated_data.get('name')
		cwe = serializer.validated_data.get('cwe')
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__application':obj,
			'name':name,
			'cwe':cwe,
			'is_false_positive':True
		}
		vuls = OpenVulnerabilityStatView().get_open_vul_query(kwargs=kwargs)		
		if not vuls.exists():
			raise QueryMisMatchError
		vuls.update(is_false_positive=False)
		return Response({'message':'Vulnerabilities are been marked as true positive'},status=status.HTTP_200_OK)

	def raise_jira(self, request, pk=None):
		"""
		Raise JIRA tickets for open vulnerabilities

		Parameters:
			pk : integer
		"""
		queryset = self.get_queryset(request.user)
		obj = get_object_or_404(queryset,pk=pk)
		serializer = RaiseJIRATicketSerializer(data=request.data,context={'request':request})
		serializer.is_valid(raise_exception=True)
		name = serializer.validated_data.get('name')
		cwe = serializer.validated_data.get('cwe')
		issuetype = serializer.validated_data.get('issuetype')
		assignee = serializer.validated_data.get('assignee')
		project_key = obj.jiraprojects.key
		kwargs = {
			'scan__application':obj,
			'name':name,
			'cwe':cwe,
			'jira_id__isnull':True
		}
		vuls = OpenVulnerabilityStatView().get_open_vul_query(kwargs=kwargs)		
		if not vuls.exists():
			raise QueryMisMatchError
		obj_dict = {
			'app_id':obj.id,
			'vul_name':name,
			'cwe':cwe,
			'project_key':project_key,
			'issuetype':issuetype,
			'assignee':assignee
		}
		raise_jira_ticket(obj_dict,request.user.org.id)
		return Response({'message':'Vulnerabilities JIRA ticket raising is in progress'},status=status.HTTP_200_OK)		
	
	def webhooks(self, request, pk=None):
		"""
		Fetch webhooks and webhook related stats

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		webhooks = obj.webhook_set.all()
		context = {}
		webhook_list = []			
		for webhook in webhooks:
			webhook_list.append({
				'fields':json.loads(serialize('json',[webhook]))[0].get('fields'),
			}) 
		context['count'] = webhooks.count()		
		context['data'] = webhook_list
		return Response(context)					


class EngagementAnalyticsView(BaseAnalyticsView):
	"""
	Analytics view for Engagement
	"""

	def get_queryset(self,user):
		"""
		Filter Engagement's by user
		"""
		return Engagement.objects.all()

	def retrieve_open(self, request, pk=None):
		"""
		Fetch open vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__engagements':obj
		}
		context, sev_context = self.get_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = OpenVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = OpenVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)

	def retrieve_closed(self, request, pk=None):
		"""
		Fetch closed vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan__engagements':obj
		}
		context, sev_context = self.get_closed_vul_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		page = self.paginate_queryset(context,request=request)
		if page is not None:
			serializer = ClosedVulSerializer(page, many=True, context={'request':request})
			return self.get_paginated_response(serializer.data)
		serializer = ClosedVulSerializer(context, many=True,context={'request':request})
		return Response(serializer.data)			

	def scans(self,request,pk=None):
		"""
		Fetch scans and scan related stats

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		scans = obj.engagements.all()
		context = {}
		scans_list = []
		for scan in scans:
			scans_list.append({
				'fields':json.loads(serialize('json',[scan]))[0].get('fields'),
				'stats':{
					'sevs':dict(scan.get_vuls_sev_count()),
					# 'vuls':scan.vulnerability_set.count()
				}
			}) 
		context['count'] = scans.count()		
		context['data'] = scans_list
		return Response(context)


class ScanAnalyticsView(BaseAnalyticsView):
	"""
	Analytics view for Scan
	"""

	def get_queryset(self,user):
		"""
		Filter Scan's by user
		"""
		return Scan.objects.all()

	def retrieve(self, request, pk=None):
		"""
		Fetch open vulnerabilities by query params

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		kwargs = {
			'scan':obj
		}
		context, sev_context = self.get_context(self.request.query_params,kwargs)		
		self.sev_context = sev_context
		return Response(context)

	def vulnerabilities(self,request,pk=None):
		"""
		Fetch scans and scan related stats

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		vuls = obj.vulnerability_set.all()
		context = {}
		vuls_list = []
		for vul in vuls:
			vuls_list.append({
				'fields':json.loads(serialize('json',[vul]))[0].get('fields'),
			}) 
		context['count'] = vuls.count()		
		context['data'] = vuls_list
		return Response(context)


class VulnerabilityAnalyticsView(BaseAnalyticsView):
	"""
	Analytics view for Vulnerability
	"""

	def get_queryset(self,user):
		"""
		Filter Vulnerability's by user
		"""
		return Vulnerability.objects.all()


	def evidences(self,request,pk=None):
		"""
		Fetch evidences for a particular vulnerability

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		evids = obj.vulnerabilityevidence_set.all()
		context = {}
		evid_list = []
		for evid in evids:
			evid_list.append({
				'fields':json.loads(serialize('json',[evid]))[0].get('fields'),
			}) 
		context['count'] = evids.count()		
		context['data'] = evid_list
		return Response(context)


	def remediations(self,request,pk=None):
		"""
		Fetch remediations for a particular vulnerability

		Parameters:
			pk : integer
		"""
		obj = self.get_queryset(request.user).get(pk=pk)
		remediations = obj.vulnerabilityremediation_set.all()
		context = {}
		remedy_list = []
		for remedy in remediations:
			remedy_list.append({
				'fields':json.loads(serialize('json',[remedy]))[0].get('fields'),
			}) 
		context['count'] = remediations.count()		
		context['data'] = remedy_list
		return Response(context)													