from django.db import models
from api.exceptions import Unauthorized


class OrganizationManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()


class OrganizationConfigurationManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('org')	 


class JiraIssueTypesManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('org')


class JiraProjectsManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('application','jira_config')


class ProjectManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('org')


class ApplicationManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('project','org')


class ScanManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().prefetch_related('engagements').select_related('application','application__org','application__project','application__project__org')	


class ScanLogManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('scan','scan__application__org','scan__application__project','scan__application__project__org')	


class EngagementManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('application','application__org','application__project','application__project__org')			


class WebhookManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('application','application__org','application__project','application__project__org')				


class VulnerabilityManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().prefetch_related('scan__engagements').select_related('scan','scan__application','scan__application__project','scan__application__project__org','scan__application__org')


class VulnerabilityEvidenceManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().prefetch_related('vul__scan__engagements').select_related('vul','vul__scan','vul__scan__application','vul__scan__application__project','vul__scan__application__project__org','vul__scan__application__org')


class VulnerabilityRemediationManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().prefetch_related('vul__scan__engagements').select_related('vul','vul__scan','vul__scan__application','vul__scan__application__project','vul__scan__application__project__org','vul__scan__application__org')


class VulnerabilityEvidenceRemediationManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().prefetch_related('evid__vul__scan__engagements').select_related('evid','evid__vul__scan','evid__vul__scan__application','evid__vul__scan__application__project','evid__vul__scan__application__project__org','evid__vul__scan__application__org')
		           