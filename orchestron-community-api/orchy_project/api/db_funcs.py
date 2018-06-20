from django.db.models import Func, Aggregate, CharField, IntegerField, DateField
import pytz

class ExtractYear(Func):
    function = 'YEAR'
    template = '%(function)s(%(expressions)s)'
    timezone = pytz.utc
    output_field = DateField()


class ExtractDate(Func):
    function = 'DATE'
    template = '%(function)s(%(expressions)s)'
    timezone = pytz.utc
    output_field = DateField()    
    

class ExtractMonth(Func):
    function = 'MONTH'
    template = 'LPAD(%(function)s(%(expressions)s),2,0)'
    timezone = pytz.utc
    output_field = DateField()
    

class ExtractMonthName(Func):
    function = 'MONTHNAME'
    template = '%(function)s(%(expressions)s)'
    timezone = pytz.utc
    output_field = DateField()      


class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(%(distinct)s%(expressions)s)'

    def __init__(self, expression, distinct=False, **extra):
        super(GroupConcat, self).__init__(
            expression,
            distinct='DISTINCT ' if distinct else '',
            output_field=CharField(),
            **extra)


class Aging(Aggregate):
    function = 'DATEDIFF'
    template = 'MAX(%(function)s(CURRENT_DATE,%(expressions)s))'

    def __init__(self, expression, **extra):
        super(Aging, self).__init__(
            expression,
            output_field=IntegerField(),
            **extra) 