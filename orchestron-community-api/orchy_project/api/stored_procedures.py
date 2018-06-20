from django.db import connection

class ReportProcedures:
    @staticmethod
    def set_max_value():
        cur = connection.cursor() 
        cur.execute('SET SESSION group_concat_max_len = 1000000;')
        cur.close()  