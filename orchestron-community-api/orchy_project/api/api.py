import os
from uuid import uuid4
from datetime import datetime
from django.utils import timezone
from base64 import b64decode,b64encode
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType as DjangoContentType
from django.contrib.auth.models import Permission as DjangoPermission
from api.models import Application, Project, Organization, Scan, Engagement, Webhook, WebhookLog, \
    Vulnerability,  VulnerabilityEvidence, VulnerabilityRemediation, VulnerabilityEvidenceRemediation, \
    User, OrganizationConfiguration, JiraIssueTypes, EmailConfiguration, ORLConfig, JiraProjects, \
    JiraUsers, ScanLog, AccessToken
from api.serializers import OrganizationSerializer, ProjectSerializer, ApplicationSerializer, ScanSerializer, \
    EngagementSerializer, WebhookSerializer, VulnerabilitySerializer, VulnerabilityEvidenceSerializer, \
    VulnerabilityRemediationSerializer, VulnerabilityEvidenceRemediationSerializer, UserSerializer, \
    OrganizationQueryParamSerializer, ProjectQueryParamSerializer, ApplicationsQueryParamSerializer, \
    OrganizationConfigurationSerializer, JiraIssueTypesSerializer, EmailConfigurationSerializer, \
    EngagementQueryParamSerializer, AssignScansSerializer, OpenVulnerabilityRemediationSerializer, \
    UpdateOpenVulnerabilitySerializer, ChangePasswordSerializer, UserProfileSerializer, \
    ScanQueryParamSerializer, ParserSerializer, JiraConnectionTestSerializer, ORLConfigSerializer, \
    JiraProjectsSerializer, ReportSerializer, CategorizeVulnerabilitySerializer,\
    DjangoSiteSerializer, ForgotPasswordSerializer, SetPasswordSerializer
from django.contrib.sites.models import Site    
from api.exceptions import Unauthorized, QueryMisMatchError, OrgConfigExistsError, OrgConfigDoesNotExists, \
    JIRAConfigNotEnabled, JIRAConfigExistsError, EmailConfigNotEnabled, EmailConfigExistsError, \
    PasswordMisMatchError, ORLConfigNotEnabled, ORLConfigExistsError, JiraProjectsConfigExistsError, JiraConfigNotEnabled
from api.utils import get_request_response, get_single_vul_context, \
    validate_allowed_files, remove_file, get_severity_by_name, get_closed_vul_context
from api.tasks import webhook_upload, webhook_process_json, forgot_email_reset, \
    parse_xmls, sync_jira_users
from api.utils import log_exception, get_severity_by_num
from api.authentications import AccessKeyAuthentication
from api.minio_utils import MinioUtil
from api.app_log import error_debug_log, info_debug_log, critical_debug_log
from django.views.static import serve
from django.http import FileResponse
import mimetypes
from django.utils.http import http_date, parse_http_date
from django.db.models import Q
from api.analytics import OpenVulnerabilityStatView, ClosedVulnerabilityStatView, UnCategorisedVulnerabilityStatView
from api.signals import *
import pytz
from django.utils import timezone
from api.orl import get_open_vul_info_from_api, get_open_vul_name_from_api
from api import jira_utils as jira
from api.db_funcs import Aging
from six import string_types
from api.orchy_logger import log
from api.stats import StatView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import binascii
from api.utils import get_ip
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class IPAdressView(APIView):
    def get(self, request):
        protocol = request.is_secure() and "https" or "http"
        return Response({'ip':request.get_host(), 'protocol':protocol})

class TokenRenewView(APIView):
    def get(self, request):
        try:
            try:
                data_dict = {
                    'access_key':binascii.hexlify(os.urandom(20)).decode(),
                    'secret_key':binascii.hexlify(os.urandom(20)).decode()
                }
                token = AccessToken.objects.get(user=request.user)
                token.access_key = data_dict.get('access_key')
                token.secret_key = data_dict.get('secret_key')
                token.save()
                # info_log('User `{0}` renewed the access token'.format(request.user.email),request)
                return Response(data_dict)
            except:
                raise Unauthorized
        except BaseException as e:
            log_exception(e)
            return Response({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetTokenView(APIView):
    def get(self, request):
        try:
            try:
                token = AccessToken.objects.get(user=request.user)                
            except AccessToken.DoesNotExist:
                data_dict = {
                    'access_key':binascii.hexlify(os.urandom(20)).decode(),
                    'secret_key':binascii.hexlify(os.urandom(20)).decode(),
                    'user':request.user
                }
                token = AccessToken.objects.create(**data_dict) 
            data_dict = {
                'access_key':token.access_key,
                'secret_key':token.secret_key
            }                
            return Response(data_dict)
        except BaseException as e:
            log_exception(e)
            return Response({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MediaServeView(APIView):

    def get(self, request, path):
        try:
            if path.startswith(settings.USER_MEDIA_URL):
                assert request.user.img == path
            elif path.startswith(settings.ORGANIZATION_MEDIA_URL):
                orgs = Organization.objects.filter(logo=path)
                assert orgs.exists()
            elif path.startswith(settings.PROJECT_MEDIA_URL):
                projects = Project.objects.filter(logo=path)
                assert projects.exists()
            elif path.startswith(settings.APPLICATION_MEDIA_URL):
                apps = Application.objects.filter(logo=path)
                assert apps.exists()
            elif path.startswith(settings.EVIDENCE_MEDIA_URL):
                evidences = VulnerabilityEvidence.objects.filter(Q(request=path) | Q(response=path) | Q(file=path) | Q(log=path))
                assert evidences.exists()
            elif path.startswith(settings.REMEDY_MEDIA_URL):
                remediations = VulnerabilityRemediation.objects.filter(file=path)
                assert remediations.exists()
            elif path.startswith(settings.EVIDENCE_REMEDY_MEDIA_URL):
                evid_remediations = VulnerabilityEvidenceRemediation.objects.filter(file=path)
                assert evid_remediations.exists()
            else:
                assert False
        except AssertionError:
            raise Unauthorized
        else:
            content_type, encoding = mimetypes.guess_type(path)
            content_type = content_type or 'application/octet-stream'
            file_obj = MinioUtil().get_file(path)
            return HttpResponse(b64encode(file_obj.read()))


class BaseView(viewsets.ModelViewSet):
    """
    This class is the base view for creating, updating, fetching and deleting the Model object
    """
    def get_queryset(self):
        """
        This view returns a queryset filtered according to the user role
        """
        object_list = self.model_class.objects.all()
        return object_list

    def retrieve(self, request, pk=None):
        """
        This view returns a particular model instance serialized data

        Parameters :
            - pk
                type : integer

                desc : Primary key of the model instance
        return type :
            json
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj,context={'request':request})
        log.info('Retrieved a single object of {0} with primary key {1}'.format(self.model_class.__name__,pk))
        return Response(serializer.data)

    def list(self, request):
        """
        This view returns a queryset of a model,
        The queryset is paginated by 5 objects

        return type :
            json
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request':request})
            log.info('Retrieved a list of objects from model {0} by {1}'.format(self.model_class.__name__,request.user))
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True,context={'request':request})
        log.info('Retrieved a list of objects from model {0} by {1}'.format(self.model_class.__name__,request.user))
        return Response(serializer.data)

    def create(self, request):
        """
        This view creates a model instance

        return type :
            json
        """
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            log.info('Created an instance of {0} by {1}'.format(self.model_class.__name__,request.user))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        This view updates a model instance

        return type :
            json
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            log.info('Updated an instance of {0} of primary key {1} by {2}'.format(self.model_class.__name__,pk,request.user))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        This view deletes a model instance

        return type :
            json
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        log.info('Deleted an instance of {0} of primary key {1} by {2}'.format(self.model_class.__name__,pk,request.user))
        return Response({'name':obj.name, 'message':'Successfully Deleted'}, status=status.HTTP_200_OK)

    def get_open_vuls(self, kwargs):
        """
        This view returns a json of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return OpenVulnerabilityStatView().vuls(kwargs=kwargs)

    def get_closed_vuls(self, kwargs):
        """
        This view returns a json of the closed vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return ClosedVulnerabilityStatView().vuls(kwargs=kwargs)

    def get_cwe_stats(self, kwargs):
        """
        This view returns a cwe statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'cwe':OpenVulnerabilityStatView().cwe_severity_count(kwargs=kwargs)}

    def get_severity_stats(self, kwargs):
        """
        This view returns a cwe statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'severity':OpenVulnerabilityStatView().severity_count(kwargs=kwargs)}

    def get_owasp_stats(self, kwargs):
        """
        This view returns a owasp statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'owasp':OpenVulnerabilityStatView().owasp_severity_count(kwargs=kwargs)}

    def get_tools_stats(self, kwargs):
        """
        This view returns a tools statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'tools':OpenVulnerabilityStatView().tool_severity_count(kwargs=kwargs)}

    def get_heatmap_stats(self, user, kwargs):
        """
        This view returns a heatmap statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'heatmap':OpenVulnerabilityStatView().heatmap(user,kwargs=kwargs)}

    def get_applications_stats(self, kwargs):
        """
        This view returns a applications statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'applications':OpenVulnerabilityStatView().application_severity_count(kwargs=kwargs)}

    def get_months_stats(self, kwargs):
        """
        This view returns a months statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'months':OpenVulnerabilityStatView().month_severity_count(kwargs=kwargs)}

    def get_grade_stats(self, kwargs):
        """
        This view returns a grade statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'grade':OpenVulnerabilityStatView().grade(kwargs=kwargs)}

    def get_ageing_stats(self, kwargs):
        """
        This view returns a ageing statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'ageing':OpenVulnerabilityStatView().aging_count(kwargs=kwargs)}

    def get_avg_ageing_stats(self, kwargs):
        """
        This view returns a average ageing statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'avg_ageing':OpenVulnerabilityStatView().avg_ageing(kwargs=kwargs)}

    def get_open_vul_stats(self, kwargs):
        """
        This view returns a count of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'open_vul_count':OpenVulnerabilityStatView().count(kwargs=kwargs)}

    def get_closed_vuls_stats(self, kwargs):
        """
        This view returns a statistics of the closed vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'closed_vul_count':ClosedVulnerabilityStatView().count(kwargs=kwargs)}


    def get_uncategorized_vul_stats(self, kwargs):
        """
        This view returns a count of the uncategorized vulnerability

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """

        return {'uncategorized':UnCategorisedVulnerabilityStatView().count(kwargs=kwargs)}


class UserView(BaseView):
    serializer_class = UserSerializer
    model_class = User

    def get_queryset(self):
        if self.request.user.is_superuser:
            object_list = self.model_class.objects.all()
        elif self.request.user.is_admin:
            object_list = self.model_class.objects.filter(is_superuser=False)
        else:
            raise Unauthorized
        return object_list

    def create(self, request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        return Response({'email':obj.email, 'message':'Successfully Deleted'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    serializer_class = UserProfileSerializer
    model_class = User

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUtilityView(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    change_password_serializer = ChangePasswordSerializer

    def change_password(self, request, email):
        email = str(b64decode(email),'utf-8')
        queryset = User.objects.filter(is_active=True,is_staff=True)
        obj = get_object_or_404(queryset, email=email)
        serializer = self.change_password_serializer(data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        if not obj.check_password(serializer.validated_data.get("old_password")):
            raise PasswordMisMatchError
        obj.set_password(serializer.validated_data.get("new_password"))
        obj.save()
        return Response({"message":"Password changed successfully"}, status=status.HTTP_200_OK)


class UserUtilityForgotView(viewsets.ViewSet):
    change_password_serializer = ForgotPasswordSerializer
    authentication_classes= ()
    permission_classes = ()

    def post(self, request):
        try:
            serializer = self.change_password_serializer(data=request.data, context={'request': self.request})
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                user = User.objects.get(email=serializer.validated_data.get('email'))
                subject = 'Reset Your Password'
                domain_override = None
                email_template_name = 'forgot_password.html'
                use_https= False
                protocol = request.is_secure() and "https" or "http"
                forgot_email_reset(serializer.validated_data.get('email'), subject, domain_override, email_template_name, use_https, protocol)
                return Response({"message": "please check your mail reset link has been sent"},
                                        status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Line no :{0} Exception {1}".format(exc_traceback.tb_lineno,e))
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



def check_token(user, token):
    try:
        return default_token_generator.check_token(user, token)
    except BaseException as e:
        return False

class PasswordUtilityView(viewsets.ViewSet):
    permission_classes = ()
    authentication_classes = ()
    set_password_serializer = SetPasswordSerializer

    def set_password(self, request, uidb64, token):
        try:
            try:
                uid = str(b64decode(uidb64), 'utf-8')
                user = User.objects.get(id=uid)
            except BaseException as e:
                user = None
            status_token = check_token(user, token)
            if user:
                serializer = self.set_password_serializer(data=request.data, context={'request': self.request})
                if serializer.is_valid():
                    new_password2 = serializer.validated_data.get('new_password2')
                    user.set_password(new_password2)
                    user.save()
                    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error':'Invalid link!'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("exceptions as e", e)
            return Response({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OrganizationOptionView(viewsets.ViewSet):

    def list(self,request):
        data = {
            'industry':[
                ('service','Service'),
                ('ecommerce','ECommerce'),('banking','Banking'),
                ('insurance','Insurance'),('manufacture','Manufacturing'),
                ('businessprocessoutsourcing','Business Process Outsourcing'),
                ('analytics','Analytics'),('telecom','Telecom'),
                ('infrastructure','Infrastructure'),('socialnetwork','Social Network'),
                ('utilities','Utilities'),('transportation','Transportation'),
                ('Retail','retail'),('finance','Financial Services'),('healthcare','Health Care'),
            ],
            'timezone':[(tz,tz) for tz in pytz.all_timezones]
        }
        return Response(data,status=status.HTTP_200_OK)


class OptionsListView(viewsets.ViewSet):

    def tools(self,request):
        data = [(t,t) for t in settings.WEBHOOK_TOOLS.keys()]
        return Response(data,status=status.HTTP_200_OK)

    def hosttypes(self,request):
        return Response(settings.HOST_TYPES,status=status.HTTP_200_OK)

    def platforms(self,request):
        return Response(settings.PLATFORMS,status=status.HTTP_200_OK)


    def permissions(self,request):
        all_model = ['scan', 'engagement', 'webhook']
        content_filter = DjangoContentType.objects.filter(app_label='api', model__in=all_model)
        all_permissions = DjangoPermission.objects.filter(content_type__in=content_filter)
        data = [(p.id,p.name) for p in all_permissions]
        return Response(data,status=status.HTTP_200_OK)


class ModelListView(viewsets.ModelViewSet):
    def get_queryset(self):
        object_list = self.model_class.objects.all()
        return object_list

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset(), many=True,context={'request':request})
        return Response(serializer.data)


class OrganizationListView(ModelListView):
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = OrganizationSerializer
    model_class = Organization


class ProjectListView(ModelListView):
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ProjectSerializer
    model_class = Project


class ApplicationListView(ModelListView):
    authentication_classes = (JSONWebTokenAuthentication,)
    model_class = Application
    serializer_class = ApplicationSerializer


class UserListView(ModelListView):
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = UserSerializer
    model_class = User


class JIRAListView(viewsets.ViewSet):

    def get_queryset(self, user):
        return Application.objects.all()

    def get_jira_config(self, user, pk):
        queryset = self.get_queryset(user)
        obj = get_object_or_404(queryset, pk=pk)
        return obj.org.jiraissuetypes

    def projects(self, request, pk):
        jira_config = self.get_jira_config(request.user, pk)
        projects = jira.get_projects(jira_config)
        data = [p.name for p in projects]
        return Response(set(data),status=status.HTTP_200_OK)

    def issuetypes(self, request, pk):
        jira_config = self.get_jira_config(request.user, pk)
        issuetypes = jira.get_issuetypes(jira_config)
        data = [p.name for p in issuetypes]
        return Response(set(data),status=status.HTTP_200_OK)

    def groups(self, request, pk):
        jira_config = self.get_jira_config(request.user, pk)
        data = jira.get_groups(jira_config)
        return Response(data,status=status.HTTP_200_OK)

    def users(self, request, pk):
        jira_config = self.get_jira_config(request.user, pk)
        data = JiraUsers.objects.filter(jira_config=jira_config).values_list('name',flat=True)
        return Response(set(data),status=status.HTTP_200_OK)


class JiraConnectionTestView(APIView):
    serializer_class = JiraConnectionTestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data.get('url')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        jira_response = jira.test_jira_connection(url,username,password)
        if not jira_response:
            return Response({'status':'Failure'},status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'status':'Success'},status=status.HTTP_200_OK)


class OrganizationView(BaseView):
    serializer_class = OrganizationSerializer
    model_class = Organization
    query_serializer = OrganizationQueryParamSerializer

    def get_projects(self, obj):
        context = {}
        pros = obj.project_set.all()
        pros_list = []
        for pro in pros:
            kwargs = {
                'scan__application__project__org':obj,
                'scan__application__project':pro
            }
            serialized_object = ProjectSerializer(pro, context={'request':self.request})
            pros_list.append({
                'fields':serialized_object.data,
                'stats':{
                    'severity_count':self.get_severity_stats(kwargs),
                    'apps_count':pro.application_set.count()
                }
            })
        context['projects_count'] = pros.count()
        context['projects'] = pros_list
        return context

    def get_users(self, obj):
        context = {}
        users = obj.user_set.all()
        users_list = []
        for user in users:
            serialized_object = UserSerializer(user, context={'request':self.request})
            users_list.append({
                'fields':serialized_object.data
            })
        context['users_count'] = users.count()
        context['users'] = users_list
        return context

    def create(self, request):
        log.info('Community will only allow single organization')
        raise Unauthorized

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj,context={'request':request})
        context = serializer.data
        query_serializer = self.query_serializer(data=self.request.query_params, context={'request':self.request})
        query_serializer.is_valid(raise_exception=True)
        projects = query_serializer.validated_data.get('projects', False)
        users = query_serializer.validated_data.get('users', False)
        cwe = query_serializer.validated_data.get('cwe',False)
        severity = query_serializer.validated_data.get('severity',False)
        owasp = query_serializer.validated_data.get('owasp',False)
        grade = query_serializer.validated_data.get('grade',False)
        tool = query_serializer.validated_data.get('tool',False)
        apps = query_serializer.validated_data.get('apps',False)
        months = query_serializer.validated_data.get('months',False)
        opened = query_serializer.validated_data.get('opened',False)
        closed = query_serializer.validated_data.get('closed',False)
        heatmap = query_serializer.validated_data.get('heatmap',False)
        ageing = query_serializer.validated_data.get('ageing',False)
        avg_ageing = query_serializer.validated_data.get('avg_ageing',False)
        uncategorized = query_serializer.validated_data.get('uncategorized', False)
        kwargs = {
            'scan__application__project__org':obj,
        }
        if cwe or tool or owasp or severity or grade or opened or apps or months or ageing or avg_ageing:
            if cwe:
                context.update(self.get_cwe_stats(kwargs))
            if tool:
                context.update(self.get_tools_stats(kwargs))
            if owasp:
                context.update(self.get_owasp_stats(kwargs))
            if severity:
                context.update(self.get_severity_stats(kwargs))
            if apps:
                context.update(self.get_applications_stats(kwargs))
            if months:
                context.update(self.get_months_stats(kwargs))
            if grade:
                context.update(self.get_grade_stats(kwargs))
            if opened:
                context.update(self.get_open_vul_stats(kwargs))
            if ageing:
                context.update(self.get_ageing_stats(kwargs))
            if avg_ageing:
                context.update(self.get_avg_ageing_stats(kwargs))
        if uncategorized:
            context.update(self.get_uncategorized_vul_stats(kwargs))
        if heatmap:
            scan_kwargs = {'application__org':obj}
            context.update(self.get_heatmap_stats(request.user,scan_kwargs))
        if closed:
            context.update(self.get_closed_vuls_stats(kwargs))
        if projects:
            context.update(self.get_projects(obj))
        if users:
            context.update(self.get_users(obj))
        return Response(context)


class DjangoSiteChangeView(BaseView):
    serializer_class = DjangoSiteSerializer    
    model_class = Site

    def get_queryset(self, pk=None):
        if pk:
            object_list = self.model_class.objects.get(pk=pk)
        else:
            object_list = self.model_class.objects.all()
        return object_list


class OrganizationConfigurationView(BaseView):
    serializer_class = OrganizationConfigurationSerializer
    model_class = OrganizationConfiguration

    def config(self, request, pk):
        obj = Organization.objects.get(pk=pk)
        config_exists = self.model_class.objects.filter(pk=pk).exists()
        if config_exists:
            raise OrgConfigExistsError
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.validated_data['org'] = obj
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        return Response({'message':'Organization Config Successfully Deleted'}, status=status.HTTP_200_OK)


class JiraIssueTypesView(BaseView):
    serializer_class = JiraIssueTypesSerializer
    model_class = JiraIssueTypes

    def config(self, request, pk):
        obj = Organization.objects.get(pk=pk)
        config = OrganizationConfiguration.objects.filter(pk=pk)
        jira_config_exists = self.model_class.objects.filter(pk=pk).exists()
        if jira_config_exists:
            raise JIRAConfigExistsError
        if not config.exists():
            raise OrgConfigDoesNotExists
        if not config[0].enable_jira:
            raise JIRAConfigNotEnabled
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.validated_data['org'] = obj
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        return Response({'message':'Organization JIRA Config Successfully Deleted'}, status=status.HTTP_200_OK)


class EmailConfigurationView(BaseView):
    serializer_class = EmailConfigurationSerializer
    model_class = EmailConfiguration

    def config(self, request, pk):
        obj = Organization.objects.get(pk=pk)
        config = OrganizationConfiguration.objects.filter(pk=pk)
        email_config_exists = self.model_class.objects.filter(pk=pk).exists()
        if email_config_exists:
            raise EmailConfigExistsError
        if not config.exists():
            raise OrgConfigDoesNotExists
        if not config[0].enable_email:
            raise EmailConfigNotEnabled
        serializer = self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.validated_data['org'] = obj
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        return Response({'message':'Organization Email Config Successfully Deleted'}, status=status.HTTP_200_OK)


class ORLConfigView(BaseView):
    serializer_class = ORLConfigSerializer
    model_class = ORLConfig

    def config(self, request, pk):
        obj = Organization.objects.get(pk=pk)
        config = OrganizationConfiguration.objects.filter(pk=pk)
        orl_config_exists = self.model_class.objects.filter(pk=pk).exists()
        if orl_config_exists:
            raise ORLConfigExistsError
        if not config.exists():
            raise OrgConfigDoesNotExists
        if not config[0].enable_orl:
            raise ORLConfigNotEnabled
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['org'] = obj
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        return Response({'message':'Organization Email Config Successfully Deleted'}, status=status.HTTP_200_OK)


class ProjectView(BaseView):
    serializer_class = ProjectSerializer
    model_class = Project
    query_serializer = ProjectQueryParamSerializer

    def create(self, request):
        """
        This view creates a project instance

        return type :
            json
        """
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_by'] = request.user.id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_applications(self, obj):
        context = {}
        apps = obj.application_set.all()
        apps_list = []
        for app in apps:
            kwargs = {
                'scan__application__project':obj,
                'scan__application':app
            }
            serialized_object = ApplicationSerializer(app, context={'request':self.request})
            apps_list.append({
                'fields':serialized_object.data,
                'stats':{
                    'severity_count':self.get_severity_stats(kwargs),
                    'scans_count':app.scan_set.count()
                }
            })
        context['applications_count'] = apps.count()
        context['applications'] = apps_list
        return context

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj,context={'request':request})
        context = serializer.data
        query_serializer = self.query_serializer(data=self.request.query_params, context={'request':self.request})
        query_serializer.is_valid(raise_exception=True)
        applications = query_serializer.validated_data.get('applications', False)
        cwe = query_serializer.validated_data.get('cwe',False)
        severity = query_serializer.validated_data.get('severity',False)
        owasp = query_serializer.validated_data.get('owasp',False)
        grade = query_serializer.validated_data.get('grade',False)
        tool = query_serializer.validated_data.get('tool',False)
        opened = query_serializer.validated_data.get('opened',False)
        closed = query_serializer.validated_data.get('closed',False)
        heatmap = query_serializer.validated_data.get('heatmap',False)
        apps = query_serializer.validated_data.get('apps',False)
        months = query_serializer.validated_data.get('months',False)
        ageing = query_serializer.validated_data.get('ageing',False)
        avg_ageing = query_serializer.validated_data.get('avg_ageing',False)
        kwargs = {
            'scan__application__project':obj,
        }
        if cwe or tool or owasp or severity or grade or opened or apps or months or ageing or avg_ageing:
            if cwe:
                context.update(self.get_cwe_stats(kwargs))
            if tool:
                context.update(self.get_tools_stats(kwargs))
            if owasp:
                context.update(self.get_owasp_stats(kwargs))
            if severity:
                context.update(self.get_severity_stats(kwargs))
            if grade:
                context.update(self.get_grade_stats(kwargs))
            if opened:
                context.update(self.get_open_vul_stats(kwargs))
            if apps:
                context.update(self.get_applications_stats(kwargs))
            if months:
                context.update(self.get_months_stats(kwargs))
            if ageing:
                context.update(self.get_ageing_stats(kwargs))
            if avg_ageing:
                context.update(self.get_avg_ageing_stats(kwargs))
        if heatmap:
            scan_kwargs = {'application__project':obj}
            context.update(self.get_heatmap_stats(request.user,scan_kwargs))
        if closed:
            context.update(self.get_closed_vuls_stats(kwargs))
        if applications:
            context.update(self.get_applications(obj))
        return Response(context)


class ApplicationView(BaseView):
    serializer_class = ApplicationSerializer
    model_class = Application
    query_serializer = ApplicationsQueryParamSerializer

    def get_scans(self, obj, assigned=None, unassigned=None):
        context = {}
        if assigned:
            scans = obj.get_assigned_scans()
        elif unassigned:
            scans = obj.get_unassigned_scans()
        else:
            scans = obj.get_all_scans()
        scans_list = []
        for scan in scans:
            serialized_object = ScanSerializer(scan, context={'request':self.request})
            scans_list.append({
                'fields':serialized_object.data,
                'stats':{
                    'severity_count':dict(scan.get_vuls_sev_count()),
                }
            })
        context['scans_count'] = scans.count()
        context['scans'] = scans_list
        return context

    def get_engagements(self, obj):
        context = {}
        engagements = obj.engagement_set.all()
        engagement_list = []
        for engagement in engagements:
            kwargs = {
                'scan__engagements':engagement
            }
            serialized_object = EngagementSerializer(engagement, context={'request':self.request})
            engagement_list.append({
                'fields':serialized_object.data,
                'stats':{
                    'severity_count':self.get_severity_stats(kwargs)
                }
            })
        context['engagements_count'] = engagements.count()
        context['engagements'] = engagement_list
        return context

    def get_webhooks(self, obj):
        context = {}
        webhooks = obj.webhook_set.all()
        webhook_list = []
        for webhook in webhooks:
            serialized_object = WebhookSerializer(webhook, context={'request':self.request})
            webhook_list.append({
                'fields':serialized_object.data,
            })
        context['webhooks_count'] = webhooks.count()
        context['webhooks'] = webhook_list
        return context

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj,context={'request':request})
        context = serializer.data
        query_serializer = self.query_serializer(data=self.request.query_params, context={'request':self.request})
        query_serializer.is_valid(raise_exception=True)
        scans = query_serializer.validated_data.get('scans', False)
        engagements = query_serializer.validated_data.get('engagements', False)
        webhooks = query_serializer.validated_data.get('webhooks', False)
        assigned = query_serializer.validated_data.get('assigned', False)
        unassigned = query_serializer.validated_data.get('unassigned', False)
        cwe = query_serializer.validated_data.get('cwe',False)
        severity = query_serializer.validated_data.get('severity',False)
        owasp = query_serializer.validated_data.get('owasp',False)
        grade = query_serializer.validated_data.get('grade',False)
        tool = query_serializer.validated_data.get('tool',False)
        opened = query_serializer.validated_data.get('opened',False)
        closed = query_serializer.validated_data.get('closed',False)
        heatmap = query_serializer.validated_data.get('heatmap',False)
        apps = query_serializer.validated_data.get('apps',False)
        ageing = query_serializer.validated_data.get('ageing',False)
        avg_ageing = query_serializer.validated_data.get('avg_ageing',False)
        months = query_serializer.validated_data.get('months',False)
        webhook = Webhook.objects.get(application=obj)
        uncategorized = query_serializer.validated_data.get('uncategorized',False)
        context['webhook_id'] = webhook.hook_id
        kwargs = {
            'scan__application':obj,
        }
        if cwe or tool or owasp or severity or grade or opened or apps or months or ageing or avg_ageing:
            if cwe:
                context.update(self.get_cwe_stats(kwargs))
            if tool:
                context.update(self.get_tools_stats(kwargs))
            if owasp:
                context.update(self.get_owasp_stats(kwargs))
            if severity:
                context.update(self.get_severity_stats(kwargs))
            if grade:
                context.update(self.get_grade_stats(kwargs))
            if opened:
                context.update(self.get_open_vul_stats(kwargs))
            if apps:
                context.update(self.get_applications_stats(kwargs))
            if months:
                context.update(self.get_months_stats(kwargs))
            if ageing:
                context.update(self.get_ageing_stats(kwargs))
            if avg_ageing:
                context.update(self.get_avg_ageing_stats(kwargs))
        if uncategorized:
            context.update(self.get_uncategorized_vul_stats(kwargs))
        if heatmap:
            scan_kwargs = {'application':obj}
            context.update(self.get_heatmap_stats(request.user,scan_kwargs))
        if closed:
            context.update(self.get_closed_vuls_stats(kwargs))
        if scans:
            if assigned:
                context.update(self.get_scans(obj, assigned=True))
            elif unassigned:
                context.update(self.get_scans(obj, unassigned=True))
            else:
                context.update(self.get_scans(obj))
        if engagements:
            context.update(self.get_engagements(obj))
        if webhooks:
            context.update(self.get_webhooks(obj))
        return Response(context)


class EngagementView(BaseView):
    serializer_class = EngagementSerializer
    model_class = Engagement
    query_serializer = EngagementQueryParamSerializer
    assign_scans_serializer = AssignScansSerializer

    def get_queryset(self):
        # kwargs = {'closed':False}
        kwargs = {}
        object_list = self.model_class.objects.filter(**kwargs)
        return object_list.order_by('-created_on')

    def get_scans(self, obj):
        context = {}
        scans = obj.engagements.all()
        scans_list = []
        for scan in scans:
            serialized_object = ScanSerializer(scan, context={'request':self.request})
            scans_list.append({
                'fields':serialized_object.data,
                'stats':{
                    'severity_count':dict(scan.get_vuls_sev_count()),
                }
            })
        context['scans_count'] = scans.count()
        context['scans'] = scans_list
        return context

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj,context={'request':request})
        context = serializer.data
        query_serializer = self.query_serializer(data=self.request.query_params, context={'request':self.request})
        query_serializer.is_valid(raise_exception=True)
        scans = query_serializer.validated_data.get('scans', False)
        if scans:
            context.update(self.get_scans(obj))
        return Response(context)

    def assign_scans(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.assign_scans_serializer(data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        scans = serializer.validated_data.get('scans')
        unassigned_scans = Scan.objects.filter(name__in=scans, application=obj.application, engagements=None)
        if not unassigned_scans.exists():
            raise QueryMisMatchError
        for scan in unassigned_scans:
            obj.engagements.add(scan.id)
        return Response({'message':'Scans assigned to Engagement {0} successfully'.format(obj.name)}, status=status.HTTP_200_OK)

    def close(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.closed = True
        obj.closed_on = timezone.now()
        obj.closed_by = request.user.id
        obj.save()
        return Response({'name':obj.name, 'message':'Engagement closed successfully'}, status=status.HTTP_200_OK)

class CategorizeVulnerability(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = CategorizeVulnerabilitySerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(context={'request': request},data=request.data)
            if serializer.is_valid():
                name = serializer.validated_data.get('name')
                common_name = serializer.validated_data.get('common_name')
                cwe = serializer.validated_data.get('cwe')
                vuls = Vulnerability.objects.filter(name=name)
                if vuls.exists():
                    vuls.update(cwe=cwe,common_name=common_name)
                    return Response({"sucess":"Categorized successfully!"},status=status.HTTP_200_OK)
                else:
                    return Response({"error":"No vuls found!"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            print("Error", e)
            return Response({'error':'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScanView(BaseView):
    serializer_class = ScanSerializer
    model_class = Scan
    query_serializer = ScanQueryParamSerializer

    def get_stats(self, obj):
        """
        This view returns a statistics of the scan related vulnerabilities

        Parameters:
            - obj
                type : Scan Object

        return type :
            json
        """
        stats = {}
        stats['severity'] = dict(obj.get_vuls_sev_count())
        stats['cwe'] = dict(obj.get_vuls_cwe_count())
        stats['owasp'] = dict(obj.get_vuls_owasp_count())
        stats['true_positive_count'] = obj.get_true_positive_vuls_count()
        stats['false_positive_count'] = obj.get_false_positive_vuls_count()
        stats['vuls_count'] = obj.get_vuls_count()
        return stats

    def get_vulnerabilities(self, vuls):
        """
        Fetch scans and scan related stats

        Parameters:
            pk : integer
        """
        context = {}
        vuls_list = []
        for vul in vuls:
            serialized_object = VulnerabilitySerializer(vul, context={'request':self.request})
            vuls_list.append({
                'fields':serialized_object.data
            })
        context['vuls_count'] = vuls.count()
        context['vuls'] = vuls_list
        return context

    def list(self, request):
        """
        This view returns a queryset of a scan,
        The queryset is paginated by 5 objects

        return type :
            json
        """
        query_serializer = self.query_serializer(data=self.request.query_params, context={'request':self.request})
        query_serializer.is_valid(raise_exception=True)
        user = query_serializer.validated_data.get('user', False)
        queryset = self.get_queryset()
        if user:
            user = User.objects.get(email=user)
            queryset = queryset.filter(created_by=user.id)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request':request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True,context={'request':request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj,context={'request':request})
        context = serializer.data
        query_serializer = self.query_serializer(data=self.request.query_params, context={'request':self.request})
        query_serializer.is_valid(raise_exception=True)
        vuls = query_serializer.validated_data.get('vuls', False)
        severity = query_serializer.validated_data.get('severity', False)
        cwe = query_serializer.validated_data.get('cwe', False)
        date = query_serializer.validated_data.get('date', False)
        stats = query_serializer.validated_data.get('stats', False)
        false = query_serializer.validated_data.get('false', False)
        true = query_serializer.validated_data.get('true', False)
        cvss = query_serializer.validated_data.get('cvss', False)
        if stats:
            context.update(self.get_stats(obj))
        if vuls:
            all_vuls = obj.vulnerability_set.all()
            context.update(self.get_vulnerabilities(all_vuls))
        elif isinstance(cvss,float):
            all_vuls = obj.vulnerability_set.filter(cvss=cvss)
            context.update(self.get_vulnerabilities(all_vuls))
        elif severity:
            severity = get_severity_by_name(severity)
            all_vuls = obj.vulnerability_set.filter(severity=severity)
            context.update(self.get_vulnerabilities(all_vuls))
        elif cwe:
            all_vuls = obj.vulnerability_set.filter(cwe=cwe)
            context.update(self.get_vulnerabilities(all_vuls))
        elif date:
            all_vuls = obj.vulnerability_set.filter(created_on__date=date)
            context.update(self.get_vulnerabilities(all_vuls))
        elif false:
            all_vuls = obj.get_false_positive_vuls()
            context.update(self.get_vulnerabilities(all_vuls))
        elif true:
            all_vuls = obj.get_true_positive_vuls()
            context.update(self.get_vulnerabilities(all_vuls))
        return Response(context)

    def create(self, request):
        """
        This view creates a model instance

        return type :
            json
        """
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['tool'] = 'Manual'
        serializer.validated_data['scan_type'] = 'Manual'
        serializer.validated_data['created_by'] = request.user.id
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """
        This view updates a model instance

        return type :
            json
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['tool'] = 'Manual'
        serializer.validated_data['scan_type'] = 'Manual'
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class WebhookView(BaseView):
    serializer_class = WebhookSerializer
    model_class = Webhook

    def get_queryset(self):
        """
        Fetch all the objects
        """
        object_list = self.model_class.objects.all()
        return object_list.order_by('-created_on')


class ParserView(viewsets.ViewSet):
    serializer_class = ParserSerializer

    def parse(self, request, pk):
        application = Application.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        result_file = serializer.validated_data.get('file')
        tool = serializer.validated_data.get('tool')
        scan_short_name = '{0}_{1}_Upload_{2}'.format(tool, application.name, timezone.now().strftime('%d_%b_%Y_%H:%M:%S'))
        obj_dict = {
            'application': application,
            'tool': tool,
            'scan_type': 'Webhook',
            'short_name': scan_short_name,
        }
        scan = Scan.objects.create(**obj_dict)
        scan_name = scan.name
        log_obj = {
            'status':'Initiated',
            'scan':scan
        }
        scan_log = ScanLog.objects.create(**log_obj)
        init_json = {
            'scan_reference':{
                'es_reference':scan_name,
            },
            'organization':{
                'name':request.user.org.name,
            },
            'host':{
                'app_uri':application.url,
                'name':application.name
            }
        }
        dir_path = settings.XML_ROOT
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        ext = result_file.name.split('.')[-1]
        complete_path = os.path.join(dir_path, '{0}.{1}'.format(str(uuid4()), ext))
        with open(complete_path, 'wb') as fp:
            fp.write(result_file.read())
        result_tool = validate_allowed_files(complete_path)
        scan_log.status = 'Uploaded'
        scan_log.save()
        if result_tool != tool:
            remove_file(complete_path)
            scan_log.status = 'Killed'
            scan_log.save()
            error_debug_log(ip=request.get_host(), user=request.user.username, event='Invalid file', status='failure')
            return Response({'Error':'Sorry!!! This is not a {0} file'.format(tool)}, status=status.HTTP_403_FORBIDDEN)
        file_format = settings.WEBHOOK_TOOLS.get(tool)
        if ext not in file_format:
            remove_file(complete_path)
            scan_log.status = 'Killed'
            scan_log.save()
            error_debug_log(ip=request.get_host(), user=request.user.username, event='Unsupported file format', status='failure')
            return Response({'Error':'Unsupported file format, supported file formats are {0}'.format(file_format)}, status=status.HTTP_403_FORBIDDEN)
        parse_xmls(None, application.id, complete_path, init_json, tool, scan_name, request.get_host(), request.user.username)
        info_debug_log(ip=request.get_host(), user=request.user.username, event='Push results', status='success')
        return Response({'message':'Parsing is in progress','scan_name':scan_name},status=status.HTTP_200_OK)


class JiraProjectsView(BaseView):
    serializer_class = JiraProjectsSerializer
    model_class = JiraProjects

    def config(self, request, pk):
        obj = Application.objects.get(pk=pk)
        config = OrganizationConfiguration.objects.filter(pk=obj.org_id)
        jira_app_config_exists = self.model_class.objects.filter(pk=pk).exists()
        if jira_app_config_exists:
            raise JIRAConfigExistsError
        if not config.exists():
            raise OrgConfigDoesNotExists
        if not config[0].enable_jira:
            raise JiraConfigNotEnabled
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['application'] = obj
        serializer.validated_data['jira_config'] = obj.org.jiraissuetypes
        serializer.save()
        sync_jira_users(obj.org_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        obj.delete()
        return Response({'message':'Application JIRA Config Successfully Deleted'}, status=status.HTTP_200_OK)


class OpenVulnerabilityBaseView(viewsets.ViewSet):

    def get_vuls(self, user, app_name, vul_name, cwe):
        app_name = str(b64decode(app_name), 'utf-8')
        vul_name = str(b64decode(vul_name), 'utf-8')
        cwe = str(b64decode(cwe), 'utf-8')
        kwargs = {
            'scan__application__name':app_name,
            'name':vul_name,
            'cwe':cwe,
            'is_remediated':False
        }
        object_list = Vulnerability.objects.annotate(open_for=Aging('created_on')).filter(**kwargs)
        return object_list


class OpenVulnerabilityView(OpenVulnerabilityBaseView):
    serializer_class = UpdateOpenVulnerabilitySerializer

    def retrieve(self, request, app_name, vul_name, cwe):
        vuls = self.get_vuls(request.user, app_name, vul_name, cwe)
        context = get_single_vul_context(vuls)
        return Response(context, status=status.HTTP_200_OK)

    def update(self, request, app_name, vul_name, cwe):
        vuls = self.get_vuls(request.user, app_name, vul_name, cwe)
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        vul = vuls[0]
        data_dict = {
            'name':serializer.validated_data.get('name', vul.name),
            'cwe':serializer.validated_data.get('cwe', vul.cwe),
            'severity':serializer.validated_data.get('severity', vul.severity),
            'owasp':serializer.validated_data.get('owasp', vul.owasp),
        }
        vuls.update(**data_dict)
        return Response({'message':'Vulnerability has been updated successfully'}, status=status.HTTP_200_OK)


class RemediateOpenVulnerabilityView(viewsets.ModelViewSet):
    serializer_class = OpenVulnerabilityRemediationSerializer

    def get_vuls(self, user, app_name, vul_name, cwe):
        app_name = str(b64decode(app_name), 'utf-8')
        vul_name = str(b64decode(vul_name), 'utf-8')
        cwe = str(b64decode(cwe), 'utf-8')
        kwargs = {
            'scan__application__name':app_name,
            'name':vul_name,
            'cwe':cwe
        }
        object_list = Vulnerability.objects.annotate(open_for=Aging('created_on')).filter(**kwargs)
        return object_list

    def create_files(self, serializer, vul):
        evid = serializer.validated_data
        image_file_name = ''
        file = evid.get('file')
        if file:
            if isinstance(file,string_types):
                image_file_name = file
            else:
                name, ext = os.path.splitext(file.name)
                image_file_name = '{0}{1}{2}'.format(settings.REMEDY_MEDIA_URL,str(uuid4()),ext)
                MinioUtil().upload_file(image_file_name,file)
        serializer.validated_data['file'] = image_file_name
        serializer.validated_data['remediated_by'] = self.request.user.id
        serializer.validated_data['remediated_on'] = timezone.now()
        serializer.validated_data['vul'] = vul
        return serializer

    def remediate(self, request, app_name, vul_name, cwe):
        vuls = self.get_vuls(request.user, app_name, vul_name, cwe)
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        for vul in vuls:
            serializer = self.create_files(serializer, vul)
            self.perform_create(serializer)
        remediations = VulnerabilityRemediation.objects.filter(vul__in=vuls)
        if remediations.exists():
            vuls.update(is_remediated=True)
        return Response({'message':'Vulnerability is been remediated'}, status=status.HTTP_200_OK)


class ClosedVulnerabilityView(viewsets.ViewSet):

    def get_vuls(self, user, app_name, vul_name, cwe):
        app_name = str(b64decode(app_name), 'utf-8')
        vul_name = str(b64decode(vul_name), 'utf-8')
        cwe = str(b64decode(cwe), 'utf-8')
        kwargs = {
            'scan__application__name':app_name,
            'name':vul_name,
            'cwe':cwe
        }
        object_list = Vulnerability.objects.annotate(open_for=Aging('created_on')).filter(**kwargs)
        return object_list

    def retrieve(self, request, app_name, vul_name, cwe):
        vuls = self.get_vuls(request.user,app_name, vul_name, cwe)
        context = get_closed_vul_context(request.get_host(),vuls)
        return Response(context, status=status.HTTP_200_OK)


class RequestResponseView(viewsets.ViewSet):

    def retrieve(self, request, app_name, vul_name, cwe, url):
        app_name = str(b64decode(app_name), 'utf-8')
        vul_name = str(b64decode(vul_name), 'utf-8')
        cwe = str(b64decode(cwe), 'utf-8')
        url = str(b64decode(url), 'utf-8')
        kwargs = {
            'scan__application__name':app_name,
            'name':vul_name,
            'cwe':cwe
        }
        vuls = Vulnerability.objects.filter(**kwargs)
        exclude_kwargs = {
            'log':None,
            'request':None,
            'response':None,
            'log':'',
            'request':'',
            'response':''
        }
        evidences = VulnerabilityEvidence.objects.filter(vul__in=vuls,url=url).exclude(**exclude_kwargs)
        if not evidences.exists():
            raise QueryMisMatchError
        context = get_request_response(request.get_host(),evidences)
        return Response(context, status=status.HTTP_200_OK)


class VulnerabilityView(BaseView):
    serializer_class = VulnerabilitySerializer
    model_class = Vulnerability

    def create(self, request):
        """
        This view creates a model instance

        return type :
            json
        """
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        cwe = serializer.validated_data.get('cwe',0)
        serializer.validated_data['tool'] = 'Manual'
        description = serializer.validated_data.get('description')
        org_obj = request.user.org
        if org_obj.orl_config_exists():
            vul_info = get_open_vul_info_from_api(cwe,org_obj)
            common_name = get_open_vul_name_from_api(cwe,org_obj)
            serializer.validated_data['common_name'] = common_name
            serializer.validated_data['dread'] = vul_info.get('dread_score')
            if not description:
                serializer.validated_data['description'] = vul_info.get('description')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        """
        This view updates a model instance

        return type :
            json
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        cwe = serializer.validated_data.get('cwe',0)
        serializer.validated_data['tool'] = 'Manual'
        description = serializer.validated_data.get('description')
        org_obj = request.user.org
        if org_obj.orl_config_exists():
            vul_info = get_open_vul_info_from_api(cwe,org_obj)
            common_name = get_open_vul_name_from_api(cwe,org_obj)
            serializer.validated_data['common_name'] = common_name
            serializer.validated_data['dread'] = vul_info.get('dread_score')
            if not description:
                serializer.validated_data['description'] = vul_info.get('description')
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class VulnerabilityEvidenceView(BaseView):
    serializer_class = VulnerabilityEvidenceSerializer
    model_class = VulnerabilityEvidence

    def create_files(self, serializer):
        evid = serializer.validated_data
        request_file_name = ''
        response_file_name = ''
        image_file_name = ''
        log_file_name = ''
        log = evid.get('log')
        file = evid.get('file')
        if file:
            name, ext = os.path.splitext(file.name)
            image_file_name = '{0}{1}{2}'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()),ext)
            MinioUtil().upload_file(image_file_name,file)
        if log:
            log_file_name = '{0}log_{1}.txt'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()))
            MinioUtil().upload_file(log_file_name,log)
        else:
            request = evid.get('request', '')
            response = evid.get('response', '')
            if request:
                request_file_name = '{0}request_{1}.txt'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()))
                MinioUtil().upload_file(request_file_name,request)
            if response:
                response_file_name = '{0}response_{1}.txt'.format(settings.EVIDENCE_MEDIA_URL,str(uuid4()))
                MinioUtil().upload_file(response_file_name,response)
        serializer.validated_data['request'] = request_file_name
        serializer.validated_data['response'] = response_file_name
        serializer.validated_data['log'] = log_file_name
        serializer.validated_data['file'] = image_file_name
        return serializer


    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        serializer = self.create_files(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(obj, data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        serializer = self.create_files(serializer)
        self.perform_update(serializer)
        return Response(serializer.data)


class VulnerabilityRemediationView(BaseView):
    serializer_class = VulnerabilityRemediationSerializer
    model_class = VulnerabilityRemediation

    def create_files(self, serializer):
        evid = serializer.validated_data
        image_file_name = ''
        file = evid.get('file')
        if file:
            name, ext = os.path.splitext(file.name)
            image_file_name = '{0}{1}{2}'.format(settings.REMEDY_MEDIA_URL,str(uuid4()),ext)
            MinioUtil().upload_file(image_file_name,file)
        serializer.validated_data['file'] = image_file_name
        serializer.validated_data['remediated_by'] = self.request.user.id
        serializer.validated_data['remediated_on'] = timezone.now()
        return serializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        serializer = self.create_files(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(obj, data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        serializer = self.create_files(serializer)
        self.perform_update(serializer)
        return Response(serializer.data)


class VulnerabilityEvidenceRemediationView(BaseView):
    serializer_class = VulnerabilityEvidenceRemediationSerializer
    model_class = VulnerabilityEvidenceRemediation

    def create_files(self, serializer):
        remedy_dir_path = settings.EVIDENCE_REMEDIATION_ROOT
        evid = serializer.validated_data
        image_file_name = ''
        file = evid.get('file')
        if file:
            name, ext = os.path.splitext(file.name)
            image_file_name = '{0}{1}{2}'.format(settings.EVIDENCE_REMEDY_MEDIA_URL,str(uuid4()), ext)
            MinioUtil().upload_file(image_file_name,file)
        serializer.validated_data['file'] = image_file_name
        serializer.validated_data['remediated_by'] = self.request.user.id
        serializer.validated_data['remediated_on'] = timezone.now()
        return serializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        serializer = self.create_files(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def update(self, request, pk=None):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(obj, data=request.data, context={'request':self.request})
        serializer.is_valid(raise_exception=True)
        serializer = self.create_files(serializer)
        self.perform_update(serializer)
        return Response(serializer.data)


class ScanStatusView(APIView):
    model_class = Scan

    def get(self, request, name):
        obj = get_object_or_404(self.model_class, name=name)
        stats = {'status':obj.scanlog.status}
        return Response(stats)


class ScanResultView(APIView):
    model_class = Scan

    def get(self, request, name):
        """
        This view returns a statistics of the scan related vulnerabilities

        Parameters:
            - obj
                type : Scan Object

        return type :
            json
        """
        obj = get_object_or_404(self.model_class, name=name)
        stats = {}
        sevs = dict(obj.get_vuls_sev_count())
        sev_dict = {}
        for k,v in sevs.items():
            s = get_severity_by_num(k)
            sev_dict[s] = v
        stats['severity'] = sev_dict
        stats['cwe'] = dict(obj.get_vuls_cwe_count())
        stats['owasp'] = dict(obj.get_vuls_owasp_count())
        stats['true_positive_count'] = obj.get_true_positive_vuls_count()
        stats['false_positive_count'] = obj.get_false_positive_vuls_count()
        stats['vuls_count'] = obj.get_vuls_count()
        return Response(stats)


class WebhookUploadView(APIView):
    authentication_classes = (JSONWebTokenAuthentication, AccessKeyAuthentication)
    permission_classes = (IsAuthenticated, )

    def create_scan(self, tool, name, application, engagement_id):
        obj_dict = {
            'application': application,
            'tool': tool,
            'scan_type': 'Webhook',
            'short_name': name,
        }
        scan = Scan.objects.create(**obj_dict)
        if engagement_id:
            engagement = Engagement.objects.filter(uniq_id=engagement_id, closed=False).last()
            if engagement:
                scan.engagements.add(engagement)
        log_obj = {
            'status':'Initiated',
            'scan':scan
        }
        scan_log = ScanLog.objects.create(**log_obj)
        return scan.name

    def save_file(self, file):
        es_reference = str(uuid4())
        dir_path = settings.XML_ROOT
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        ext = file.name.split('.')[-1]
        complete_path = os.path.join(dir_path, '{0}.{1}'.format(es_reference, ext))
        with open(complete_path, 'wb') as fp:
            fp.write(file.read())
        return complete_path

    def get_tool(self, json=None, file_path=None):
        if json:
            tool = json.get('vuls', {}).get('tool', 'Unknown')
        elif file_path:
            tool = validate_allowed_files(file_path)
        else:
            tool = None
        return tool

    def post(self, request, pk, format=None):
        try:
            obj = get_object_or_404(Webhook,pk=pk)
            json_dict = request.data.get('vuls')
            result_file = request.data.get('file')
            if json_dict or result_file:
                application = obj.application
                engagement_id = request.META.get('HTTP_ENGAGEMENT', '')
                webhook_scan_name = request.META.get('HTTP_SCAN', '')
                log_dict = {
                    'file_upload_event':False,
                    'file_upload_exception':'',
                    'file_upload_datetime':timezone.now(),
                    'webhook':obj
                }
                log_obj = WebhookLog.objects.create(**log_dict)
                if json_dict:
                    webhook_tool = self.get_tool(json=json_dict, file_path=None)
                else:
                    complete_path = self.save_file(result_file)
                    webhook_tool = self.get_tool(json=None, file_path=complete_path)
                if webhook_scan_name:
                    scan_short_name = webhook_scan_name
                else:
                    scan_short_name = '{0}_{1}_webhook_{2}'.format(webhook_tool, application.name, timezone.now().strftime('%d_%b_%Y_%H:%M:%S'))
                scan_name = self.create_scan(webhook_tool, scan_short_name, application, engagement_id)
                init_json = {
                    'scan_reference':{
                        'es_reference':scan_name,
                    },
                    'organization':{
                        'name':request.user.org.name,
                    },
                    'host':{
                        'app_uri':application.url,
                        'name':application.name,
                    }
                }
                if json_dict:
                    vulnerabilities = request.data.get('vuls', {}).get('vulnerabilities')
                    if not vulnerabilities:
                        return Response({'Error':'No data to process'}, status=status.HTTP_403_FORBIDDEN)
                    webhook_process_json(request.user, application.id, json_dict, init_json, webhook_tool, scan_name, request.get_host(), request.user.username, log_obj.id)
                    return Response({'Success':'Result pushed successfully', 'scan_id':scan_name}, status=status.HTTP_200_OK)
                else:
                    valid_file = webhook_tool in settings.WEBHOOK_TOOLS.keys()
                    ext = complete_path.split('.')[-1]
                    if valid_file:
                        file_format = settings.WEBHOOK_TOOLS.get(webhook_tool)
                        if ext not in file_format:
                            remove_file(complete_path)
                            return Response({'Error':'Unsupported file format, supported file formats are {0}'.format(file_format)}, status=status.HTTP_403_FORBIDDEN)
                        webhook_upload(None, application.id, complete_path, init_json, webhook_tool, scan_name, request.get_host(), request.user.username, log_obj.id)
                        return Response({'Success':'Result pushed successfully', 'scan_id':scan_name}, status=status.HTTP_200_OK)
                    else:
                        remove_file(complete_path)
                        return Response({'Error':'Sorry!!! This file is not supported'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'Error':'Sorry!!! Could not process the event'}, status=status.HTTP_403_FORBIDDEN)
        except BaseException as e:
            log_exception(e)
            return Response({'Error':'Unable to push the result'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class WebhookUploadView(APIView):

#     def post(self, request, pk, format=None):
#         obj = Webhook.objects.get(pk=pk)
#         log_dict = {
#             'file_upload_event':False,
#             'file_upload_exception':'',
#             'file_upload_datetime':timezone.now(),
#             'webhook':obj
#         }
#         log_obj = WebhookLog.objects.create(**log_dict)
#         try:
#             es_reference = str(uuid4())
#             engagement_id = request.META.get('HTTP_ENGAGEMENT', '')
#             webhook_scan_name = request.META.get('HTTP_SCAN', '')
#             if webhook_scan_name:
#                 scan_short_name = webhook_scan_name
#             else:
#                 scan_short_name = '{0}_{1}_webhook_{2}'.format(obj.tool, obj.application.name, timezone.now().strftime('%d_%b_%Y_%H:%M:%S'))
#             obj_dict = {
#                 'application': obj.application,
#                 'tool': obj.tool,
#                 'scan_type': 'Webhook',
#                 'short_name': scan_short_name,
#             }
#             scan = Scan.objects.create(**obj_dict)
#             if engagement_id:
#                 engagement = Engagement.objects.filter(uniq_id=engagement_id, closed=False).last()
#                 if engagement:
#                     scan.engagements.add(engagement)
#             scan_name = scan.name
#             init_json = {
#                 'scan_reference':{
#                     'es_reference':scan_name,
#                 },
#                 'organization':{
#                     'name':request.user.org.name,
#                 },
#                 'host':{
#                     'app_uri':obj.application.url,
#                     'name':obj.application.name,
#                 }
#             }
#             if obj.tool == 'Orchestron JSON':
#                 json_dict = request.data.get('vuls')
#                 if not json_dict or request.content_type != 'application/json':
#                     error_debug_log(ip=request.get_host(), user=request.user.username, event='No data to process', status='failure')
#                     return Response({'Error':'No data to process'}, status=status.HTTP_403_FORBIDDEN)
#                 tool = request.data.get('vuls', {}).get('tool', 'Unknown')
#                 vulnerabilities = request.data.get('vuls', {}).get('vulnerabilities')
#                 if not vulnerabilities:
#                     error_debug_log(ip=request.get_host(), user=request.user.username, event='No data to process', status='failure')
#                     return Response({'Error':'No data to process'}, status=status.HTTP_403_FORBIDDEN)
#                 webhook_process_json(request.user, obj.application.id, json_dict, init_json, tool, scan_name, request.get_host(), request.user.username, log_obj.id)
#             else:
#                 result_file = request.data.get('file')
#                 dir_path = settings.XML_ROOT
#                 if not os.path.isdir(dir_path):
#                     os.mkdir(dir_path)
#                 ext = result_file.name.split('.')[-1]
#                 complete_path = os.path.join(dir_path, '{0}.{1}'.format(es_reference, ext))
#                 with open(complete_path, 'wb') as fp:
#                     fp.write(result_file.read())
#                 tool = validate_allowed_files(complete_path)
#                 if tool != obj.tool:
#                     remove_file(complete_path)
#                     error_debug_log(ip=request.get_host(), user=request.user.username, event='Invalid file', status='failure')
#                     return Response({'Error':'Sorry!!! This is not a {0} file'.format(obj.tool)}, status=status.HTTP_403_FORBIDDEN)
#                 file_format = settings.WEBHOOK_TOOLS.get(obj.tool)
#                 if ext not in file_format:
#                     error_debug_log(ip=request.get_host(), user=request.user.username, event='Unsupported file format', status='failure')
#                     return Response({'Error':'Unsupported file format, supported file formats are {0}'.format(file_format)}, status=status.HTTP_403_FORBIDDEN)
#                 webhook_upload(None, obj.application.id, complete_path, init_json, obj.tool, scan_name, request.get_host(), request.user.username, log_obj.id)
#                 info_debug_log(ip=request.get_host(), user=request.user.username, event='Push results', status='success')
#             return Response({'Success':'Result pushed successfully', 'scan_id':scan_name}, status=status.HTTP_200_OK)
#         except BaseException as e:
#             critical_debug_log(ip=request.get_host(), user=request.user.username, event=e, status='failure')
#             log_obj.file_upload_exception = e
#             log_obj.file_upload_datetime = timezone.now()
#             log_obj.save()
#             log_exception(e)
#             return Response({'Error':'Unable to push the result'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




import sys
class ExecutiveReportView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ReportSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(context={'request': request},data=request.data)
            if serializer.is_valid():
                apps = serializer.validated_data.get('apps')
                proj = serializer.validated_data.get('proj')
                eng = serializer.validated_data.get('eng')
                sev = serializer.validated_data.get('sev')
                tools = serializer.validated_data.get('tools')
                kwargs = {}
                if apps:
                    kwargs['scan__application__in'] = apps
                if proj:
                    kwargs['scan__application__project__in'] = proj
                if eng:
                    kwargs['scan__engagements__in'] = eng
                if sev:
                    kwargs['severity__in'] = sev
                if tools:
                    kwargs['tool__in'] = tools
                if kwargs:
                    user = request.user
                    s = StatView()
                    open_vuls = s.get_open_vuls_abstract(user,kwargs=kwargs)
                    paginator = Paginator(open_vuls, 5)
                    page = request.GET.get('page')
                    try:
                        vuls_dict = paginator.page(page)
                    except PageNotAnInteger:
                        vuls_dict = paginator.page(1)
                    except EmptyPage:
                        vuls_dict = paginator.page(paginator.num_pages)
                    data_dict = dict()
                    data_dict.update({'open_vuls':list(vuls_dict)})
                    data_dict.update(s.get_vul_entry_date(user,kwargs=kwargs))
                    data_dict.update(s.get_severity_stats(user,kwargs=kwargs))
                    data_dict.update(s.get_owasp_stats(user,kwargs=kwargs))
                    data_dict.update(s.get_ageing_stats(user,kwargs=kwargs))
                    # data_dict.update(s.get_avg_ageing_stats(user,kwargs=kwargs))
                    data_dict.update(s.get_open_vul_stats(user,kwargs=kwargs))
                    data_dict.update(s.get_closed_vuls_stats(user,kwargs=kwargs))
                    data_dict.update(s.get_false_positive_stats(user,kwargs=kwargs))
                    # data_dict.update(s.get_months_stats(user,kwargs=kwargs))
                    # info_log('Executive report generated',request)
                    return Response(data_dict, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            # log_exception(e, request=request, module_name=inspect.stack()[0][3])
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("Line no :{0} Exception {1}".format(exc_traceback.tb_lineno,e))
