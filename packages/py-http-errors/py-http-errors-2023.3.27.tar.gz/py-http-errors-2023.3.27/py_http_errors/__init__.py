import inspect
from ._base import (
    get_http_status_mapping,
    HTTP_STATUS_ENUMS_MAP,
    BaseApiError,
    JsonResponse,
)

__version__ = "2023.3.27"


class ApiExceptionMocker():
    ## mock the origin exception to BaseException
    """
    from utils.exceptions import ApiExceptionWrapper
    import sqlalchemy.exc as sqlerrors
    sql_errors = ApiExceptionWrapper(sqlerrors, index_name='ApiMysqlError')    
    """
    MOCKED_PREFIX = 'ApiErrMocked'
    BaseException = BaseApiError

    def __init__(self, namespace, mocked_prefix=MOCKED_PREFIX, description_prefix=''):
        # @namespace: module/package/class , eg: 
        self.namespace = namespace
        self._prefix = mocked_prefix
        self.description_prefix = description_prefix

    def __getattr__(self, name):
        err = AttributeError(f"[{self._prefix}] not found attribute({name}) at {self.namespace}")
        v = getattr(self.namespace, name, err)
        if inspect.isclass(name):
            if issubclass(v, Exception):
                desc = getattr(v, "description", str(v))
                code = getattr(v, "code", id(v))
                vtag = f"{self._prefix}.{name}"
                return type(
                    vtag,
                    (self.BaseException, v),
                    {'msg': f"{self.description_prefix}{desc}", 'code': code}
                )
        elif v is None:
            raise err
        return v
