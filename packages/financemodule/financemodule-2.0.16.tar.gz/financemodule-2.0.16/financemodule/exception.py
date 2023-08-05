from rest_framework.exceptions import APIException

class ModelNotFound(APIException):
    status_code = 404
    default_detail = 'field model_type should be of value as either FINANCING or REPAYMENT'
    default_code = 'model_object_not_found'


class InterestAccountNotFound(APIException):
    status_code = 404
    default_detail = 'Interest account not found'
    default_code = 'Interest account not found'


class InterestTypeNotFound(APIException):
    status_code = 404
    default_detail = 'field interest rate type should be of value as either OWNPARTY or COUNTERPARTY'
    default_code = 'model_object_not_found'


class AccountInformException(APIException):
    status_code = 404
    default_detail = 'The field account_info_2 should contain value as "currency":"ABC"}'
    default_code = 'account_info_data_mismatch'


class InterestRateTypeException(APIException):
    status_code = 404
    default_detail = 'Interest Rate type not found should be as LIBOR or EURIBOR or SOFR '
    default_code = 'account_info_data_mismatch'



class ValueTypeException(APIException):
    status_code = 404
    default_detail = 'The account_info_1 and account_info_2 field should be value in JSON'
    default_code = 'value type exception'



class RepaymentValuesException(APIException):
    status_code = 404
    default_detail = 'repayment currency or repayment amount field not found'
    default_code = 'repayment type exception'


class ProgramNotFound(APIException):
    status_code = 404
    default_detail = 'Program typr not found should be APF / RF / DF'
    default_code = 'program type not found'



class InterestPaidBy(APIException):
    status_code = 404
    default_detail = 'Interest paid by not found , must be OWNPARTY or COUNTERPART'
    default_code = 'interest paid by not found'