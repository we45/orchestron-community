import math
from collections import Counter
from rest_framework import viewsets
from django.db.models import Sum,Count, Max, Min, Value as V, Q, F
from django.db.models.functions import Concat
from api.models import Vulnerability, Scan, Application, Project, Engagement
from api.db_funcs import GroupConcat, Aging, ExtractMonth, ExtractYear
from django.conf import settings
from api.stored_procedures import ReportProcedures



class UncategorizedVulnerabilityStatView(viewsets.ViewSet):
    def uncategorized_vuls_query(self, user, kwargs={}, exclude_kwargs={}):
        new_kwargs = kwargs
        new_kwargs['is_false_positive'] = kwargs.get('is_false_positive',False)
        uncategorize_vuls = Vulnerability.objects.filter(cwe=0,is_remediated=False).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .values('common_name')\
            .distinct()\
            .order_by('common_name')
        return uncategorize_vuls

    def vuls(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.uncategorized_vuls_query(user, kwargs, exclude_kwargs)
        open_vuls = raw_vuls.annotate(tools=GroupConcat('tool',distinct=True),\
                count=Count('name',distinct=True),\
                apps=GroupConcat('scan__application__name',distinct=True),\
                open_for=Max(Aging('created_on')),\
                names=GroupConcat(Concat('name',V('###'),'scan__application__name',V('###'),V('###')),distinct=True))
        return open_vuls.values('tools','severity','apps','common_name','open_for','names','cwe','count').order_by('-severity')

    def count(self, user, kwargs={}, exclude_kwargs={}):
        vuls = self.uncategorized_vuls_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return sum(dict(Counter(vuls)).values())

    def severity_count(self, user, kwargs={}, exclude_kwargs={}):
        sevs = self.uncategorized_vuls_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return dict(Counter(sevs))


class FalsePositiveVulnerabilityStatView(viewsets.ViewSet):
    def get_open_vul_fp_query(self, user, kwargs={}, exclude_kwargs={}):
        open_vuls = Vulnerability.objects.filter(is_false_positive=True,is_remediated=False).filter(**kwargs)\
            .exclude(**exclude_kwargs)\
            .values('common_name')\
            .distinct()\
            .order_by('common_name')
        return open_vuls

    def vuls(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_fp_query(user, kwargs, exclude_kwargs)
        open_vuls = raw_vuls.annotate(tools=GroupConcat('tool',distinct=True),\
                count=Count('name',distinct=True),\
                apps=GroupConcat('scan__application__name',distinct=True),\
                open_for=Max(Aging('created_on')),\
                names=GroupConcat(Concat('name',V('###'),'scan__application__name',V('###'),V('###')),distinct=True))
        return open_vuls.values('tools','severity','apps','common_name','open_for','names','cwe','count').order_by('-severity')

    def count(self, user, kwargs={}, exclude_kwargs={}):
        vuls = self.get_open_vul_fp_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return sum(dict(Counter(vuls)).values())

    def severity_count(self, user, kwargs={}, exclude_kwargs={}):
        sevs = self.get_open_vul_fp_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return dict(Counter(sevs))


class OpenVulnerabilityToolTypeStatView(viewsets.ViewSet):
    def get_open_vul_query(self, user, kwargs={}, exclude_kwargs={}):
        new_kwargs = kwargs
        new_kwargs['is_false_positive'] = kwargs.get('is_false_positive',False)
        open_vuls = Vulnerability.objects.filter(is_remediated=False).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .values('common_name')\
            .distinct()\
            .order_by('common_name')
        return open_vuls

    def get_tool_type_stats(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_query(user, kwargs, exclude_kwargs)
        tool_types = raw_vuls.values('tool').annotate(total=Count('tool')).order_by('total')               
        data_dict = {}
        for tool in tool_types:
            tool_type = settings.TOOL_TYPES.get(tool.get('tool'))
            if tool_type not in data_dict:
                data_dict[tool_type] = 0
            data_dict[tool_type] = data_dict[tool_type] + tool.get('total')
        total_vuls = 0
        for tool in tool_types:
            total_vuls += tool.get('total',0)        
        percentage_dict = {}
        if total_vuls:
            for k,v in data_dict.items():
                percentage = (v/total_vuls) * 100
                percentage_dict[k] = percentage
        return percentage_dict


class OpenVulnerabilityStatView(viewsets.ViewSet):
    def get_open_vul_cwe_query(self, user, kwargs={}, exclude_kwargs={}):
        new_kwargs = kwargs
        new_kwargs['is_false_positive'] = kwargs.get('is_false_positive',False)
        open_vuls = Vulnerability.objects.filter(is_remediated=False).filter(**new_kwargs)\
            .exclude(**exclude_kwargs)\
            .values('cwe')\
            .distinct()\
            .order_by('cwe')\
            .values_list('cwe',flat=True)
        return open_vuls

    def get_open_vul_query(self, user, kwargs={}, exclude_kwargs={}):
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

    def vuls(self, user, kwargs={}, exclude_kwargs={}):
        ReportProcedures.set_max_value()
        raw_vuls = self.get_open_vul_query(kwargs, exclude_kwargs)     
        open_vuls = raw_vuls.annotate(tools=GroupConcat('tool',distinct=True),\
                count=Count('name',distinct=True),\
                apps=GroupConcat('scan__application__name',distinct=True),\
                common_name=GroupConcat('common_name',distinct=True),\
                open_for=Aging('created_on'),\
                names=GroupConcat(Concat('name',V('###'),'scan__application__name',V('###'),'jira_id',V('###'),'jira_issue_status'),distinct=True))         
        return open_vuls.values('tools','severity','apps','common_name','open_for','names','cwe','count').order_by('-severity')

    def abstract_vuls(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_query(user, kwargs, exclude_kwargs)
        open_vuls = raw_vuls.annotate(apps=GroupConcat('scan__application__name',distinct=True),\
                names=GroupConcat(Concat('name',V('###'),'scan__application__name',V('###'),V('###')),distinct=True))
        return open_vuls.values('severity','apps','common_name','names','cwe').order_by('-severity')

    def vul_entry_date(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_query(user, kwargs, exclude_kwargs)
        dates = raw_vuls.values_list('created_on',flat=True)
        if dates:
            date = min(dates)
            min_date = date.strftime("%d-%b-%Y")
            return min_date
        return ''

    def avg_ageing(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_query(user, kwargs, exclude_kwargs)
        open_vuls = raw_vuls.annotate(open_for=Max(Aging('created_on')))
        avg_ageing_val = 0
        if open_vuls:
            all_ageing_count = [v.get('open_for') for v in open_vuls]
            if all_ageing_count:
                avg_ageing_val = math.ceil(sum(all_ageing_count)/len(all_ageing_count))
        return avg_ageing_val

    def count(self, user, kwargs={}, exclude_kwargs={}):
        vuls = self.get_open_vul_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return sum(dict(Counter(vuls)).values())

    def severity_count(self, user, kwargs={}, exclude_kwargs={}):
        sevs = self.get_open_vul_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return dict(Counter(sevs))

    def cwe_severity_count(self, user, kwargs={}, exclude_kwargs={}):
        cwes = self.get_open_vul_query(user, kwargs, exclude_kwargs).values_list('cwe','severity')
        return self.process_list(cwes)

    def tool_severity_count(self, user, kwargs={}, exclude_kwargs={}):
        tools = self.get_open_vul_query(user, kwargs, exclude_kwargs).values_list('tool','severity')
        return self.process_list(tools)

    def owasp_severity_count(self, user, kwargs={}, exclude_kwargs={}):
        owasps = self.get_open_vul_query(user, kwargs, exclude_kwargs).values_list('owasp','severity')
        return self.process_list(owasps)

    def scan_severity_count(self, user, kwargs={}, exclude_kwargs={}):
        scans = self.get_open_vul_query(user, kwargs, exclude_kwargs)\
        .values_list('scan__short_name','severity')
        return self.process_list(scans)

    def application_severity_count(self, user, kwargs={}, exclude_kwargs={}):
        applications = self.get_open_vul_query(user, kwargs, exclude_kwargs).values_list('scan__application__id','scan__application__name','severity')
        return self.process_apps(applications)

    def month_severity_count(self, user, kwargs={}, exclude_kwargs={}):
        raw_vuls = self.get_open_vul_query(user, kwargs, exclude_kwargs).order_by('created_on')
        # months = raw_vuls.annotate(month=Concat(V('01'),V('-'),ExtractMonth('created_on'),V('-'),ExtractYear('created_on'))\
        #     ,severity=F('severity'))\
        #     .values_list('month','severity')
        months = raw_vuls.annotate(
            month=Concat(V('01'), V('-'), ExtractMonth('created_on'), V('-'), ExtractYear('created_on')) \
            , severity=F('severity')) \
            .values_list('month', 'severity')
        return self.process_list(months)

    def aging_count(self, user, kwargs={}, exclude_kwargs={}):
        aging_list = self.get_open_vul_query(user, kwargs, exclude_kwargs)\
        .annotate(open_for=Aging('created_on'))\
        .values_list('open_for','severity')
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
    def get_closed_vul_query(self, user, kwargs, exclude_kwargs):
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

    def vuls(self, user, kwargs={}, exclude_kwargs={}):
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

    def count(self, user, kwargs={}, exclude_kwargs={}):
        vuls = self.get_closed_vul_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return sum(dict(Counter(vuls)).values())

    def severity_count(self, user, kwargs={}, exclude_kwargs={}):
        sevs = self.get_closed_vul_query(user, kwargs, exclude_kwargs).values_list('severity',flat=True)
        return dict(Counter(sevs))


class StatView(viewsets.ViewSet):
    def get_open_vuls(self, user, kwargs):
        """
        This view returns a json of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return OpenVulnerabilityStatView().vuls(user, kwargs=kwargs)

    def get_open_vuls_abstract(self, user, kwargs):
        """
        This view returns a json of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return OpenVulnerabilityStatView().abstract_vuls(user, kwargs=kwargs)

    def get_vul_entry_date(self, user, kwargs):
        """
        This view returns a json of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'entry_date':OpenVulnerabilityStatView().vul_entry_date(user, kwargs=kwargs)}

    def get_closed_vuls(self, user, kwargs):
        """
        This view returns a json of the closed vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return ClosedVulnerabilityStatView().vuls(user, kwargs=kwargs)

    def get_cwe_stats(self, user, kwargs):
        """
        This view returns a cwe statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'cwe':OpenVulnerabilityStatView().cwe_severity_count(user, kwargs=kwargs)}

    def get_severity_stats(self, user, kwargs):
        """
        This view returns a cwe statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'severity':OpenVulnerabilityStatView().severity_count(user, kwargs=kwargs)}

    def get_owasp_stats(self, user, kwargs):
        """
        This view returns a owasp statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'owasp':OpenVulnerabilityStatView().owasp_severity_count(user, kwargs=kwargs)}

    def get_tools_stats(self, user, kwargs):
        """
        This view returns a tools statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'tools':OpenVulnerabilityStatView().tool_severity_count(user, kwargs=kwargs)}

    def get_heatmap_stats(self, user, kwargs):
        """
        This view returns a heatmap statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'heatmap':OpenVulnerabilityStatView().heatmap(user,user, kwargs=kwargs)}

    def get_applications_stats(self, user, kwargs):
        """
        This view returns a applications statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'applications':OpenVulnerabilityStatView().application_severity_count(user, kwargs=kwargs)}

    def get_months_stats(self, user, kwargs):
        """
        This view returns a months statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'months':OpenVulnerabilityStatView().month_severity_count(user, kwargs=kwargs)}

    def get_ageing_stats(self, user, kwargs):
        """
        This view returns a ageing statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'ageing':OpenVulnerabilityStatView().aging_count(user, kwargs=kwargs)}

    def get_avg_ageing_stats(self, user, kwargs):
        """
        This view returns a average ageing statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'avg_ageing':OpenVulnerabilityStatView().avg_ageing(user, kwargs=kwargs)}

    def get_uncategorized_vul_stats(self, user, kwargs):
        """
        This view returns a average ageing statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'uncategorized':UncategorizedVulnerabilityStatView().count(user, kwargs=kwargs)}

    def get_tool_type_stats(self, user, kwargs):
        """
        This view returns a average ageing statistics of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'tool_types':OpenVulnerabilityToolTypeStatView().get_tool_type_stats(user, kwargs=kwargs)}        

    def get_false_positive_stats(self, user, kwargs):
        """
        This view returns a count of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        new_kwargs = kwargs
        new_kwargs['is_false_positive'] = True
        return {'false_positive_count':OpenVulnerabilityStatView().count(user, kwargs=new_kwargs)}

    def get_open_vul_stats(self, user, kwargs):
        """
        This view returns a count of the open vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'open_vul_count':OpenVulnerabilityStatView().count(user, kwargs=kwargs)}

    def get_closed_vuls_stats(self, user, kwargs):
        """
        This view returns a statistics of the closed vulnerabilities

        Parameters:
            - kwargs
                type : json

        return type :
            json
        """
        return {'closed_vul_count':ClosedVulnerabilityStatView().count(user, kwargs=kwargs)}
