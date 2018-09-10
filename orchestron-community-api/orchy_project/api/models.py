import os
import json
import pytz
from datetime import datetime, time
from uuid import uuid4
from hashlib import sha256
from random import getrandbits
from collections import Counter
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin, Permission
from django.utils.translation import ugettext_lazy as _
from django.core.validators import URLValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import connection
from api.exceptions import Unauthorized,AuthenticationError
from api.ciphertext_manager import JIRACipher, EmailCipher
from api import jira_utils as jira 
from api.email_utils import test_email_connection
from api.storage import OverwriteStorage
from api.managers import OrganizationManager, ProjectManager, ApplicationManager, VulnerabilityManager, ScanManager, \
    EngagementManager, WebhookManager, VulnerabilityEvidenceManager, VulnerabilityRemediationManager, \
    VulnerabilityEvidenceRemediationManager, OrganizationConfigurationManager, JiraIssueTypesManager, \
    EmailConfigurationManager, ORLConfigurationManager, JiraProjectsManager, ScanLogManager


def get_uniq_name():
    uuid = uuid4()
    timstamp = datetime.now()
    name = sha256('{0}{1}'.format(uuid,timstamp).encode('utf-8')).hexdigest()
    return name


class BaseModel(models.Model):
    """
    Creates a model of temporal information regarding creation and updation
    """
    created_on = models.DateTimeField(default=timezone.now)
    edited_on = models.DateTimeField(auto_now= True)


    class Meta:
        abstract = True
        ordering = ('-created_on',)


class Organization(BaseModel):
    """
    Creates a model for the Organization type, timezones, locations, logos and
    their contact information.
    """
    ORGANIZATION_TYPE = [('','Select Organization Type'),('service','Service'),
        ('ecommerce','ECommerce'),('banking','Banking'),
        ('insurance','Insurance'),('manufacture','Manufacturing'),
        ('businessprocessoutsourcing','Business Process Outsourcing'),
        ('analytics','Analytics'),('telecom','Telecom'),
        ('infrastructure','Infrastructure'),('socialnetwork','Social Network'),
        ('utilities','Utilities'),('transportation','Transportation'),
        ('Retail','retail'),('finance','Financial Services'),('healthcare','Health Care'),
    ]
    l = [('','Select TimeZone')]
    TIMEZONE_LIST = l + [(tz,tz) for tz in pytz.all_timezones]
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="{0}%Y/%m/%d".format(settings.ORGANIZATION_MEDIA_URL), blank=True, null=True, storage=OverwriteStorage())
    industry = models.CharField(max_length=50,choices=ORGANIZATION_TYPE)
    timezone = models.CharField(max_length=100,choices=TIMEZONE_LIST)
    contact = models.CharField(max_length=50, null=True, blank=True)
    super_org = models.BooleanField(default=False)
    end_date = models.DateField()
    start_date = models.DateField()
    num_users = models.IntegerField(default=0)
    num_apps = models.IntegerField(default=0)
    num_scans = models.IntegerField(default=0)
    num_engagements = models.IntegerField(default=0)
    num_projects = models.IntegerField(default=0)
    objects = OrganizationManager()

    def __str__(self):
        return self.name

    def get_logo_filename(i):
        """
        Returns the path to the logo of a particular organization
        """
        ipath = settings.MEDIA_ROOT
        logopath = os.path.join(ipath,i.logo.name)
        return str(logopath)

    def update_user_count(self):
        if self.user_remaining >0:
            self.user_remaining = self.user_remaining - 1
            self.save()

    def update_project_count(self):
        if self.project_remaining >0:
            self.project_remaining = self.project_remaining - 1
            self.save()

    def update_application_count(self):
        if self.application_remaining >0:
            self.application_remaining = self.application_remaining - 1
            self.save()

    def update_scans_count(self):
        if scans_remaining >0:
            self.scans_remaining = self.scans_remaining +1
            self.save()

    def orl_config_exists(self):
        if hasattr(self,'organizationconfiguration'):
            if self.organizationconfiguration.enable_orl:
                if hasattr(self,'orlconfig'):
                    if self.orlconfig.org:
                        return True
        return False            

    def jira_config_exists(self):
        if hasattr(self,'organizationconfiguration'):
            if self.organizationconfiguration.enable_jira:
                if hasattr(self,'jiraissuetypes'):
                    if self.jiraissuetypes.org:
                        return True
        return False                    


class UserManager(BaseUserManager):
    """
    This class manages user operations such as creating normal and super user
    """
    def _create_user(self, username, org, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, org=org,first_name=username.title(),
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        user = self._create_user(username, email, password, False, False,**extra_fields)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        try:
            org = Organization.objects.get(id=1)
        except:
        	today = datetime.today().date()
        	org_dict = {
        		'timezone':'UTC',
        		'name':'Admin Organization',
        		'location':'Bengaluru',
        		'contact':'Abhay Bhargav',
        		'industry':'service',
        		'super_org':True,
        		'start_date':today,
        		'end_date':datetime(today.year,today.month + 1,today.day).date(),
        	}
        	org = Organization.objects.create(**org_dict)
        user = self._create_user(username, org, email, password, True, True,**extra_fields)
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_queryset(self):
        return super().get_queryset().select_related('org').filter(is_active=True,is_staff=True)             


class User(AbstractBaseUser, PermissionsMixin):
    """
    This view creates a model of User by abstracting the base user model
    """
    org = models.ForeignKey(Organization,on_delete=models.CASCADE)
    username = models.CharField(_('username'), max_length=30, unique=False,error_messages={'unique':"This email has already been added."},\
        help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    email = models.EmailField(_('email address'),unique=True, max_length=255)
    is_staff = models.BooleanField(_('staff status'), default=False,
    help_text=_('Designates whether the user can log into this admin site.'))
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    img = models.ImageField(upload_to="{0}%Y/%m/%d".format(settings.USER_MEDIA_URL), null=True, blank=True, storage=OverwriteStorage())
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-id',)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class Project(BaseModel):
    """
    Creates a model to hold information about the organization, the team and the
    managers, contact information , duration of the Project and its
    objective
    """
    org = models.ForeignKey(Organization,on_delete=models.CASCADE)
    managers = models.ManyToManyField(User, related_name="managers", blank=True)
    name = models.CharField(max_length=100, unique=True)
    objective = models.TextField(blank=True,null=True)
    logo = models.ImageField(upload_to="{0}%Y/%m/%d".format(settings.PROJECT_MEDIA_URL), null=True, blank=True, storage=OverwriteStorage())
    created_by = models.CharField(max_length=25,blank=True,null=True)
    objects = ProjectManager()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('add_application','Add Application'),
        )
        ordering = ('-created_on',)


class Application(BaseModel):
    """
    Creates a model which contains details regarding the application type, corresponding
    project, name, URL and its IP address, information regarding its version and the
    platform on which the user intends to use this tool
    """
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    type_hosts = [(h,h) for h in settings.HOST_TYPES]
    name = models.CharField(max_length=200,unique=True)
    ipv4 = models.GenericIPAddressField(max_length=200,blank=True,null=True)
    os_info = models.TextField(null=True,blank=True)
    host_type = models.CharField(max_length=100, null=True, choices=type_hosts)
    url = models.CharField(max_length=255,validators=[URLValidator()])
    # app_version = models.CharField(max_length=30, null=True, blank=True)
    type_platforms = [(p,p) for p in settings.PLATFORMS]
    platform_tags = models.CharField(max_length=100, null=True, blank=True, choices=type_platforms)
    org = models.ForeignKey(Organization,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=25,blank=True,null=True)
    logo = models.ImageField(upload_to="{0}%Y/%m/%d".format(settings.APPLICATION_MEDIA_URL), null=True, blank=True, storage=OverwriteStorage())
    objects = ApplicationManager()

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ()
        permissions = (
            ('update_application','Update Application'),
            ('delete_application','Delete Application'),
            ('export_analytics', 'Export Analytics'),
        )
        ordering = ('-id',)

    def get_assigned_scans(self):
        return self.scan_set.exclude(engagements=None)

    def get_unassigned_scans(self):
        return self.scan_set.filter(engagements=None)

    def get_all_scans(self):
        return self.scan_set.all()      
       

class Engagement(BaseModel):
    """
    This view creates a model of Engagement
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, null=True)
    stop_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=25,blank=True,null=True)
    edited_by = models.CharField(max_length=25,blank=True,null=True)
    closed = models.BooleanField(default=False)
    closed_on = models.DateTimeField(blank=True,null=True)
    closed_by = models.CharField(max_length=25,blank=True,null=True)
    uniq_id = models.UUIDField(db_column = 'uniq_id', default = uuid4)
    objects = EngagementManager()

    def __str__(self):
        return self.name

    class Meta:
        # default_permissions=()
        permissions = (
            ('copy_engagement_id', 'Copy Engagement Id'),
            ('close_engagement', 'Close Engagement'),
            ('add_scans_to_engagement', 'Add Scans to Engagement')
        )


class Scan(BaseModel):
    """
    Creates a model which contains information about the application scan preferences,
    details of the application, preferred tool, elastic search reference ID and the name
    """
    scan_choices = [('Manual','Manual'),('Webhook','Webhook'),('Client','Client')]
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    engagements = models.ManyToManyField(Engagement, related_name = 'engagements', blank=True)
    tool = models.CharField(max_length=50)
    scan_type = models.CharField(max_length=20,choices=scan_choices)
    name = models.CharField(max_length=255, default=get_uniq_name)
    created_by = models.CharField(max_length=25,blank=True,null=True)
    short_name = models.CharField(max_length=255)
    objects = ScanManager()

    def __str__(self):
        return '%s_%s'%(self.tool,self.scan_type)


    class Meta:
        default_permissions = ()
        permissions = (
            ('add_scan', 'Create Scan'),
            ('delete_scan', 'Delete Scan'),
        )
        ordering = ('-id',)

    def get_vuls_sev_count(self):
        vuls = self.vulnerability_set.values('severity')
        return Counter([v['severity'] for v in vuls])

    def get_vuls_owasp_count(self):
        vuls = self.vulnerability_set.values('owasp')
        return Counter([v['owasp'] for v in vuls])                         

    def get_vuls_cwe_count(self):
        vuls = self.vulnerability_set.values('cwe')
        return Counter([v['cwe'] for v in vuls])

    def get_true_positive_vuls(self):
        return self.vulnerability_set.filter(is_false_positive=False)

    def get_false_positive_vuls(self):
        return self.vulnerability_set.filter(is_false_positive=True)        

    def get_true_positive_vuls_count(self):
        vuls = self.get_true_positive_vuls()
        return vuls.count()

    def get_false_positive_vuls_count(self):
        vuls = self.get_false_positive_vuls()
        return vuls.count()

    def get_vuls_count(self):
        vuls = self.vulnerability_set.all()
        return vuls.count()        


class ScanLog(BaseModel):
    """
    This view creates a model of ScanLog
    """
    status_choices = [(c,c) for c in settings.SCAN_STATUS]
    status = models.CharField(max_length=50,choices=status_choices)
    scan = models.OneToOneField(Scan,on_delete=models.CASCADE,primary_key=True)
    objects = ScanLogManager()

    def __str__(self):
        return unicode(self.scan.name)


class Webhook(BaseModel):
    """
    This view creates a model of Webhook
    """
    name = models.CharField(max_length=255,unique=True)
    hook_id = models.UUIDField(db_column = 'hook_id', primary_key=True, default = uuid4, editable = False)
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    tool_choices = [(t,t) for t in settings.WEBHOOK_TOOLS]
    tool = models.CharField(max_length=255,choices=tool_choices,null=True, blank=True)
    objects = WebhookManager()

    def __str__(self):
        return self.name


class WebhookLog(BaseModel):
    """
    This view creates a model of WebhookLog
    """
    file_upload_event = models.BooleanField(default=True)
    file_upload_exception = models.TextField(blank=True,null=True)
    file_upload_datetime = models.DateTimeField(default=timezone.now)
    vul_process_event = models.BooleanField(default=True)
    vul_process_exception = models.TextField(blank=True,null=True)
    vul_process_datetime = models.DateTimeField(default=timezone.now)
    scan_process_event = models.BooleanField(default=True)
    scan_process_exception = models.TextField(blank=True,null=True)
    scan_process_datetime = models.DateTimeField(default=timezone.now)
    scan_id = models.CharField(max_length=255,blank=True,null=True)
    webhook = models.ForeignKey(Webhook,on_delete=models.CASCADE)

    def __str__(self):
        return unicode(self.webhook.hook_id)


class Vulnerability(BaseModel):
    """
    This view creates a model of Vulnerability
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    remediation = models.TextField(blank=True,null=True)
    tool = models.CharField(max_length=255)
    confidence = models.CharField(max_length=255,blank=True,null=True)
    severity = models.PositiveIntegerField(default=1,validators=[MaxValueValidator(4),MinValueValidator(0)])
    vul_type = models.CharField(max_length=255,blank=True,null=True)
    owasp = models.CharField(max_length=255)
    cvss = models.FloatField(blank=True,null=True)
    cwe = models.PositiveIntegerField(validators=[MaxValueValidator(9999),MinValueValidator(0)])
    scan = models.ForeignKey(Scan,on_delete=models.CASCADE)
    is_false_positive = models.BooleanField(default=False)
    is_remediated = models.BooleanField(default=False)
    jira_id = models.CharField(max_length=255,blank=True,null=True)
    jira_issue_status = models.CharField(max_length=255,blank=True,null=True)
    dread = models.FloatField(blank=True, null=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    objects = VulnerabilityManager()

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('update_vulnerability', 'Modify Vulnerability'),
            ('close_vulnerability', 'Close Vulnerability'),
        )   
        ordering = ('-id',)   
    

class VulnerabilityRemediation(BaseModel):
    """
    This view creates a model of VulnerabilityRemediation
    """
    vul = models.ForeignKey(Vulnerability,on_delete=models.CASCADE)
    description = models.CharField(max_length=250, null=True, blank=True)
    file = models.CharField(max_length=100, null=True, blank=True)
    remediated_by = models.CharField(max_length=250,blank=True,null=True)
    remediated_on = models.DateTimeField(auto_now_add=True)
    objects = VulnerabilityRemediationManager()


class VulnerabilityEvidence(BaseModel):
    """
    This view creates a model of VulnerabilityEvidence
    """
    vul = models.ForeignKey(Vulnerability,on_delete=models.CASCADE)
    is_remediated = models.BooleanField(default=False)
    url = models.TextField(null=True,blank=True,validators=[URLValidator()])
    name = models.CharField(max_length=250, null=True, blank=True)
    attack = models.TextField(null=True, blank=True)
    file = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    request = models.TextField(blank=True,null=True)
    response = models.TextField(blank=True,null=True)
    is_false_positive = models.BooleanField(default=False)
    log = models.TextField(blank=True,null=True)
    issue_type = models.CharField(max_length=100, null=True, blank=True)
    param = models.TextField(blank=True,null=True)
    payload = models.TextField(blank=True,null=True)
    line_number = models.CharField(max_length=200, null=True, blank=True)
    line_range = models.CharField(max_length=200, null=True, blank=True)
    file_path = models.TextField(blank=True,null=True)
    code_snippet = models.TextField(blank=True,null=True)
    method_name = models.TextField(blank=True,null=True)
    objects = VulnerabilityEvidenceManager()

    def __str__(self):
        return self.url


class VulnerabilityEvidenceRemediation(BaseModel):
    """
    This view creates a model of VulnerabilityEvidenceRemediation
    """
    evid = models.ForeignKey(VulnerabilityEvidence,on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    file = models.CharField(max_length=100, null=True, blank=True)
    remediated_by = models.CharField(max_length=30,blank=True,null=True)
    remediated_on = models.DateTimeField(auto_now_add=True)
    type_choices = [('Closed - Not Applicable','Closed - Not Applicable'),('Resolved','Resolved'),('Closed - Risk Accepted','Closed - Risk Accepted')]
    remediation_type = models.CharField(max_length=100,choices=type_choices)
    objects = VulnerabilityEvidenceRemediationManager()


class OrganizationConfiguration(BaseModel):
    """
    This view creates a model of OrganizationConfiguration
    """
    enable_jira = models.BooleanField(default=False)
    enable_email = models.BooleanField(default=False)
    enable_orl = models.BooleanField(default=False)
    org = models.OneToOneField(Organization,on_delete=models.CASCADE,primary_key=True)
    objects = OrganizationConfigurationManager()

    def __str__(self):
        return self.org.name

    class Meta:
        ordering = ('-org',)              


class ORLConfig(BaseModel):
    host = models.CharField(max_length=200)
    port = models.CharField(max_length=200)
    protocol = models.CharField(max_length=200,choices=[('http','http'),('https','https')])
    org = models.OneToOneField(Organization,on_delete=models.CASCADE,primary_key=True)
    objects = ORLConfigurationManager()

    def __unicode__(self):
        return self.org.name

    def get_config_url(self):
        return '{0}://{1}:{2}'.format(self.protocol,self.host,self.port)                


class JiraIssueTypes(BaseModel):
    """
    Creates a model to hold JIRA credentials, the application urls and details about
    the project managers (owners) of a particular organization
    """
    url = models.URLField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    issue_types = models.TextField(null=True, blank=True)
    org = models.OneToOneField(Organization,on_delete=models.CASCADE,primary_key=True)
    created_by = models.CharField(max_length=25,blank=True,null=True)
    objects = JiraIssueTypesManager()

    def __str__(self):
        return self.org.name

    class Meta:
        ordering = ('-org',)    

    def save(self, *args, **kwargs):
        url = self.url
        username = self.username
        password = self.password
        jira_response = jira.test_jira_connection(url,username,password)
        if not jira_response:
            raise AuthenticationError
        else:
            cipher = JIRACipher()
            self.username = cipher.encrypt(username)
            self.password = cipher.encrypt(password)
            super(JiraIssueTypes, self).save(*args, **kwargs)             


class JiraProjects(BaseModel):
    """
    This view creates a model of JiraProjects
    """
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    jira_config = models.ForeignKey(JiraIssueTypes,on_delete=models.CASCADE)
    application = models.OneToOneField(Application,on_delete=models.CASCADE,primary_key=True)
    objects = JiraProjectsManager()

    def __str__(self):
        return '{0} - {1}'.format(self.name,self.key)


class JiraUsers(BaseModel):
    """
    This view creates a model of JiraUsers
    """
    name = models.CharField(max_length=200)
    group = models.CharField(max_length=200)
    jira_config = models.ForeignKey(JiraIssueTypes,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class JiraConfigurations(BaseModel):
    """
    This view creates a model of JiraConfigurations
    """
    name = models.CharField(max_length=200)
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    jira_project = models.CharField(max_length=200)
    jira_assignee = models.CharField(max_length=200)
    mapping_to_high = models.CharField(max_length=200)
    mapping_to_medium = models.CharField(max_length=200)
    mapping_to_low = models.CharField(max_length=200)
    mapping_to_info = models.CharField(max_length=200)
    org = models.ForeignKey(Organization,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class EmailConfiguration(BaseModel):
    """
    This view creates a model of EmailConfiguration
    """
    host = models.CharField(max_length=200)
    port = models.CharField(max_length=250)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    from_email = models.EmailField(max_length=200,default='Orchestron')
    display_name = models.CharField(max_length=200,default='Orchestron')
    certs = models.CharField(max_length=100, null=True, blank=True)
    org = models.OneToOneField(Organization,on_delete=models.CASCADE, primary_key=True)
    objects = EmailConfigurationManager()

    def __str__(self):
        return self.host

    class Meta:
        ordering = ('-org',)

    def save(self, *args, **kwargs):
        email_response = test_email_connection(self.host,self.port,self.username,self.password,self.certs,self.from_email)
        if not email_response:
            raise AuthenticationError
        cipher = EmailCipher()
        self.username = cipher.encrypt(self.username)
        self.password = cipher.encrypt(self.password)
        self.host = cipher.encrypt(self.host)
        self.port = cipher.encrypt(self.port)
        super(EmailConfiguration, self).save(*args, **kwargs)           
