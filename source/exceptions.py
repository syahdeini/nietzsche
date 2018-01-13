from sanic.exceptions import add_status_code, SanicException
from sanic.response import STATUS_CODES

@add_status_code(422)
class FailClv(SanicException):
    def __init__(self, _message="cannot calculate clv"):
        self.status=422
        super().__init__(message=_message, status_code=self.status)


class NoCustomerFound(Exception):
     def __init__(self):
        Exception.__init__(self,"customer data is not found, please check customer id")

class OrderCsvNotFound(Exception):
    def __init__(self, path):
        Exception.__init__(self,"file order.csv not found in" + path)


