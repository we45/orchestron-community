from rest_framework.exceptions import APIException

class MinioCredentialsError(APIException):
    status_code = 400
    default_detail = 'Unable to upload files at this moment'
    default_code = 'bad_request'


class MinioNoFileError(APIException):
    status_code = 404
    default_detail = 'File not found'
    default_code = 'not found'


class MinioResponseError(APIException):
    status_code = 400
    default_detail = 'Unable to upload files at this moment'
    default_code = 'bad_request'


class Unauthorized(APIException):
    status_code = 403
    default_detail = 'User is unauthorized to perform this action'
    default_code = 'forbidden'


class AuthenticationError(APIException):
    status_code = 403
    default_detail = 'Unable to authenticate'
    default_code = 'forbidden' 


class Notfound(APIException):
    status_code = 404
    default_detail = 'Object not found'
    default_code = 'not found' 


class QueryMisMatchError(APIException):
    status_code = 404
    default_detail = 'Data does not meet necessary conditions'
    default_code = 'invalid' 


class PasswordMisMatchError(APIException):
    status_code = 404
    default_detail = 'Wrong Password'
    default_code = 'invalid'     


class OrgConfigExistsError(APIException):
    status_code = 400
    default_detail = 'Organization Config already exists'
    default_code = 'bad_request'


class OrgConfigDoesNotExists(APIException):
    status_code = 404
    default_detail = 'Organization Config does not exist'
    default_code = 'not found'


class JIRAConfigNotEnabled(APIException):
    status_code = 404
    default_detail = 'Organization JIRA Config is not enabled'
    default_code = 'invalid'


class JIRAConfigExistsError(APIException):
    status_code = 400
    default_detail = 'Organization JIRA Config already exists'
    default_code = 'bad_request'    


class EmailConfigNotEnabled(APIException):
    status_code = 404
    default_detail = 'Organization Email Config is not enabled'
    default_code = 'invalid' 


class EmailConfigExistsError(APIException):
    status_code = 400
    default_detail = 'Organization Email Config already exists'
    default_code = 'bad_request'                           


class ORLConfigNotEnabled(APIException):
    status_code = 404
    default_detail = 'Organization ORL Config is not enabled'
    default_code = 'invalid' 


class ORLConfigExistsError(APIException):
    status_code = 400
    default_detail = 'Organization ORL Config already exists'
    default_code = 'bad_request' 


class JiraConfigNotEnabled(APIException):
    status_code = 404
    default_detail = 'Organization Jira Config is not enabled'
    default_code = 'invalid'


class JiraProjectsConfigExistsError(APIException):
    status_code = 400
    default_detail = 'Application JIRA Config already exists'
    default_code = 'bad_request'
  