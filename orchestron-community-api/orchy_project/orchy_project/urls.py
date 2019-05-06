from django.urls import re_path,include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from api.api import OrganizationView, ProjectView, ApplicationView, ScanView, EngagementView, \
	WebhookView, WebhookUploadView, VulnerabilityView, VulnerabilityEvidenceView, \
    VulnerabilityRemediationView, VulnerabilityEvidenceRemediationView, UserView, OrganizationConfigurationView, \
    JiraIssueTypesView, EmailConfigurationView, OpenVulnerabilityView, RequestResponseView, RemediateOpenVulnerabilityView,\
    ClosedVulnerabilityView, UserUtilityView, UserProfileView, MediaServeView, OrganizationOptionView, \
    OptionsListView, ParserView, JiraConnectionTestView, \
    ORLConfigView, ScanResultView, JiraProjectsView, JIRAListView, \
    ScanStatusView, OrganizationListView, ProjectListView, ApplicationListView, UserListView, ExecutiveReportView,\
    CategorizeVulnerability, TokenRenewView, GetTokenView
from rest_framework_jwt.views import obtain_jwt_token
from api.analytics import OrganizationAnalyticsView, ProjectAnalyticsView, ApplicationAnalyticsView, \
    EngagementAnalyticsView, ScanAnalyticsView, VulnerabilityAnalyticsView



urlpatterns = [
    re_path(r'^api/renew/token/$', TokenRenewView.as_view()),
    re_path(r'^api/get/token/$', GetTokenView.as_view()),
    re_path(r'^media/(?P<path>.*)$', MediaServeView.as_view()),
    re_path(r'^api/user/password/change/(?P<email>.*)/$', UserUtilityView.as_view({'post':'change_password'})),
    re_path(r'^api/user/token/', obtain_jwt_token),
    re_path(r'^api/user/profile/', UserProfileView.as_view()),

    re_path(r'^api/users/list/$', UserListView.as_view({'get':'list'}),name='user_list'),
    re_path(r'^api/organizations/list/$', OrganizationListView.as_view({'get':'list'}),name='org_list'),
    re_path(r'^api/projects/list/$', ProjectListView.as_view({'get':'list'}),name='pro_list'),
    re_path(r'^api/applications/list/$', ApplicationListView.as_view({'get':'list'}),name='app_list'),

    re_path(r'^api/users/$', UserView.as_view({'get':'list','put':'create'}),name='user'),
    re_path(r'^api/users/(?P<pk>\d+)/$', UserView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_user'),

    re_path(r'^api/tools/$', OptionsListView.as_view({'get':'tools'}),name='tools'),
    re_path(r'^api/hosttypes/$', OptionsListView.as_view({'get':'hosttypes'}),name='hosttypes'),
    re_path(r'^api/platforms/$', OptionsListView.as_view({'get':'platforms'}),name='platforms'),
    re_path(r'^api/permissions/$', OptionsListView.as_view({'get':'permissions'}),name='permissions'),

    re_path(r'^api/openvul/catgorize/$', CategorizeVulnerability.as_view(),name='catgorize_open_vul'),

    re_path(r'^api/organizations/options/$', OrganizationOptionView.as_view({'get':'list'}),name='org_options'),
    re_path(r'^api/organizations/$', OrganizationView.as_view({'get':'list','put':'create'}),name='org'),
    re_path(r'^api/organizations/(?P<pk>\d+)/$', OrganizationView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_org'),
    re_path(r'^api/organizations/(?P<pk>\d+)/projects/$',  OrganizationAnalyticsView.as_view({'get':'projects'}),name='org_pro_openvul'),
    re_path(r'^api/organizations/(?P<pk>\d+)/config/$',  OrganizationConfigurationView.as_view({'get':'retrieve','put':'config','post':'update','delete':'destroy'}),name='ind_org_config'),
    re_path(r'^api/organizations/(?P<pk>\d+)/jira/$',  JiraIssueTypesView.as_view({'get':'retrieve','put':'config','post':'update','delete':'destroy'}),name='ind_org_jira_config'),
    re_path(r'^api/organizations/(?P<pk>\d+)/email/$',  EmailConfigurationView.as_view({'get':'retrieve','put':'config','post':'update','delete':'destroy'}),name='ind_org_email_config'),
    re_path(r'^api/organizations/(?P<pk>\d+)/orl/$',  ORLConfigView.as_view({'get':'retrieve','put':'config','post':'update','delete':'destroy'}),name='ind_org_orl_config'),

    re_path(r'^api/jira/connection/test/$',  JiraConnectionTestView.as_view(),name='test_jira_con'),

    re_path(r'^api/projects/$', ProjectView.as_view({'get':'list','put':'create'}),name='pro'),
    re_path(r'^api/projects/(?P<pk>\d+)/$', ProjectView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_pro'),
    re_path(r'^api/projects/(?P<pk>\d+)/applications/$', ProjectAnalyticsView.as_view({'get':'applications'}),name='pro_app_openvul'),


    re_path(r'^api/applications/$', ApplicationView.as_view({'get':'list','put':'create'}),name='app'),
    re_path(r'^api/applications/(?P<pk>\d+)/$', ApplicationView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_app'),
    re_path(r'^api/applications/(?P<pk>\d+)/scans/$', ApplicationAnalyticsView.as_view({'get':'scans'}),name='app_scan'),
    re_path(r'^api/applications/(?P<pk>\d+)/engagements/$', ApplicationAnalyticsView.as_view({'get':'engagements'}),name='app_engagements'),
    re_path(r'^api/applications/(?P<pk>\d+)/webhooks/$', ApplicationAnalyticsView.as_view({'get':'webhooks'}),name='app_webhooks'),
    re_path(r'^api/applications/(?P<pk>\d+)/jira/$',  JiraProjectsView.as_view({'get':'retrieve','put':'config','post':'update','delete':'destroy'}),name='ind_app_jira_config'),
    re_path(r'^api/applications/(?P<pk>\d+)/parsers/$',  ParserView.as_view({'post':'parse'}),name='ind_app_parsers'),

    re_path(r'^api/jira/projects/(?P<pk>\d+)/$', JIRAListView.as_view({'get':'projects'}),name='jira_projects'),
    re_path(r'^api/jira/groups/(?P<pk>\d+)/$', JIRAListView.as_view({'get':'groups'}),name='jira_groups'),
    re_path(r'^api/jira/users/(?P<pk>\d+)/$', JIRAListView.as_view({'get':'users'}),name='jira_users'),
    re_path(r'^api/jira/issuetypes/(?P<pk>\d+)/$', JIRAListView.as_view({'get':'issuetypes'}),name='jira_issuetypes'),

    re_path(r'^api/scans/$', ScanView.as_view({'get':'list','put':'create'}),name='scan'),
    re_path(r'^api/scans/(?P<pk>\d+)/$', ScanView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_scan'),
    re_path(r'^api/scans/(?P<pk>\d+)/vulnerabilities/$', ScanAnalyticsView.as_view({'get':'vulnerabilities'}),name='ind_scan_vuls'),

    re_path(r'^api/engagements/$', EngagementView.as_view({'get':'list','put':'create'}),name='engagement'),
    re_path(r'^api/engagements/(?P<pk>\d+)/$', EngagementView.as_view({'get':'retrieve','post':'update','delete':'destroy','patch':'close'}),name='ind_engagement'),
    re_path(r'^api/engagements/(?P<pk>\d+)/scans/assign/$', EngagementView.as_view({'post':'assign_scans'}),name='assign_scans_to_engagement'),

    re_path(r'^api/webhooks/post/(?P<pk>.*)/$', WebhookUploadView.as_view(),name='webhook_upload'),
    re_path(r'^api/webhooks/result/(?P<name>.*)/$', ScanResultView.as_view(),name='webhook_result'),
    re_path(r'^api/webhooks/(?P<pk>.*)/$', WebhookView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_webhook'),
    re_path(r'^api/webhooks/$', WebhookView.as_view({'get':'list','put':'create'}),name='webhook'),
    re_path(r'^api/scan/status/(?P<name>.*)/$', ScanStatusView.as_view(),name='ind_scan_status'),

    re_path(r'^api/vulnerabilities/$', VulnerabilityView.as_view({'get':'list','put':'create'}),name='vul'),
    re_path(r'^api/vulnerabilities/(?P<pk>\d+)/$', VulnerabilityView.as_view({'get':'retrieve','delete':'destroy'}),name='ind_vul'),
    re_path(r'^api/vulnerabilities/(?P<pk>\d+)/evidences/$', VulnerabilityAnalyticsView.as_view({'get':'evidences'}),name='ind_vul_evids'),
    re_path(r'^api/vulnerabilities/(?P<pk>\d+)/remediations/$', VulnerabilityAnalyticsView.as_view({'get':'remediations'}),name='ind_vul_remedys'),

    re_path(r'^api/evidences/$', VulnerabilityEvidenceView.as_view({'get':'list','put':'create'}),name='evidence'),
    re_path(r'^api/evidences/(?P<pk>\d+)/$', VulnerabilityEvidenceView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_evidence'),

    re_path(r'^api/remediations/$', VulnerabilityRemediationView.as_view({'get':'list','put':'create'}),name='remediation'),
    re_path(r'^api/remediations/(?P<pk>\d+)/$', VulnerabilityRemediationView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_remediation'),

    re_path(r'^api/evidremediations/$', VulnerabilityEvidenceRemediationView.as_view({'get':'list','put':'create'}),name='evidremediation'),
    re_path(r'^api/evidremediations/(?P<pk>\d+)/$', VulnerabilityEvidenceRemediationView.as_view({'get':'retrieve','post':'update','delete':'destroy'}),name='ind_evidremediation'),

    re_path(r'^api/openvul/org/(?P<pk>\d+)/$', OrganizationAnalyticsView.as_view({'get':'retrieve_open'}),name='org_openvul'),

    re_path(r'^api/openvul/project/(?P<pk>\d+)/$', ProjectAnalyticsView.as_view({'get':'retrieve_open'}),name='pro_openvul'),

    re_path(r'^api/openvul/app/bulk/mark/false/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'mark_bulk_vuls_false_positive'}),name='app_bulkvul_mark_false_positive'),
    re_path(r'^api/openvul/app/bulk/mark/true/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'mark_bulk_vuls_true_positive'}),name='app_bulkvul_mark_true_positive'),
    re_path(r'^api/openvul/app/bulk/raise/jira/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'raise_bulk_jira'}),name='app_bulkvul_raise_jira'),
    re_path(r'^api/openvul/app/mark/false/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'mark_open_vul_false_positive'}),name='app_openvul_mark_false_positive'),
    re_path(r'^api/openvul/app/mark/true/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'mark_open_vul_true_positive'}),name='app_openvul_mark_true_positive'),
    re_path(r'^api/openvul/app/raise/jira/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'raise_jira'}),name='app_openvul_raise_jira'),
    re_path(r'^api/openvul/app/bulk/delete/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'post':'bulk_delete'}),name='app_bulk_delete'),
    re_path(r'^api/openvul/app/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'get':'retrieve_open'}),name='app_openvul'),
    re_path(r'^api/openvul/remediate/(?P<app_name>.*)/(?P<vul_name>.*)/(?P<cwe>.*)/$', RemediateOpenVulnerabilityView.as_view({'post':'remediate'}),name='remediate_ind_openvul'),
    re_path(r'^api/openvul/(?P<app_name>.*)/(?P<vul_name>.*)/(?P<cwe>.*)/(?P<url>.*)/$', RequestResponseView.as_view({'get':'retrieve'}),name='app_ind_openvul'),
    re_path(r'^api/openvul/(?P<app_name>.*)/(?P<vul_name>.*)/(?P<cwe>.*)/$', OpenVulnerabilityView.as_view({'get':'retrieve','post':'update'}),name='app_ind_openvul'),

    re_path(r'^api/openvul/engagement/(?P<pk>\d+)/$', EngagementAnalyticsView.as_view({'get':'retrieve_open'}),name='eng_openvul'),

    re_path(r'^api/closedvul/org/(?P<pk>\d+)/$', OrganizationAnalyticsView.as_view({'get':'retrieve_closed'}),name='org_closedvul'),

    re_path(r'^api/closedvul/project/(?P<pk>\d+)/$', ProjectAnalyticsView.as_view({'get':'retrieve_closed'}),name='pro_closedvul'),

    re_path(r'^api/closedvul/app/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'get':'retrieve_closed'}),name='app_closedvul'),

    re_path(r'^api/closedvul/engagement/(?P<pk>\d+)/$', EngagementAnalyticsView.as_view({'get':'retrieve_closed'}),name='eng_closedvul'),

    re_path(r'^api/closedvul/(?P<app_name>.*)/(?P<vul_name>.*)/(?P<cwe>.*)/$', ClosedVulnerabilityView.as_view({'get':'retrieve'}),name='app_ind_closedvul'),

    re_path(r'^api/report/executive/$', ExecutiveReportView.as_view(),name='executive_report'),
    re_path(r'^api/uncategorize/org/(?P<pk>\d+)/$', OrganizationAnalyticsView.as_view({'get':'retrieve_uncategorized'}),name='org_uncategorize_openvul'),
    re_path(r'^api/uncategorize/app/(?P<pk>\d+)/$', ApplicationAnalyticsView.as_view({'get':'retrieve_uncategorized'}),name='app_uncategorised'),
]

# handler404 = page_not_found
