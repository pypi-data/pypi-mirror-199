from datetime import datetime
from http import HTTPStatus
import uuid
import os


def get_http_status_mapping():
    # Enum has a member called _value2member_map_
    # ( which is undocumented and may be changed/removed in future python versions)
    res = getattr(HTTPStatus, "_value2member_map_", None)
    if res is None:
        res = dict((m.value, m) for m in HTTPStatus)
    return res


_env = os.environ.setdefault
HTTP_STATUS_ENUMS_MAP = get_http_status_mapping()


class BaseApiError(Exception):
    """
    usage sample:
    ```
    class ApiError(BaseApiError, HTTPException):
        _request_id = None
        kwargs = None
        errno = 40000
        code = 400
        msg = ""

    ```
    """
    errno = 40000  # customize 5-digit-number, status_code * 100
    status = 400
    msg = ""
    result_ok = None

    def __init__(self, msg="", result_ok=None, **kwargs):
        super().__init__()
        self.errno = kwargs.pop("errno", self.errno)
        self._request_id = kwargs.pop("request_id", None)
        status = kwargs.get("status", self.errno // 100)  # http status code, return type: int
        self._set_http_status(status)
        self.description = self._describe_status()
        self.kwargs = kwargs
        self.msg = msg or self.msg
        self.result_ok = result_ok

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        desc = f"[{self.__class__.__name__}:{self.errno}:{self.request_id}] {self.msg}"
        return f"{desc} => ({self.status_msg}:{self.status})"

    def _describe_status(self):
        status_enum = HTTP_STATUS_ENUMS_MAP.get(self.status, None)
        if status_enum is not None:
            return f"[{status_enum.name}:{self.errno}] {status_enum.description}"
        return f"[???ERROR:{self.errno}] unknown http status !!! => 400"

    def _set_http_status(self, status: int):
        status_enum = HTTP_STATUS_ENUMS_MAP.get(status)
        if not status_enum:
            self.status_msg = ""
        else:
            self.status = status
            self.status_msg = status_enum.name

    @staticmethod
    def new_request_id(prefix="x"):
        ct = datetime.now().strftime("%m%d%H%M%S")
        rnd = str(uuid.uuid4())[:4]
        return ''.join([prefix, ct, "_", rnd])

    @property
    def request_id(self):
        if not self._request_id:
            self._request_id = self.new_request_id()
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        self._request_id = value

    def to_dict(self, **kwargs):
        data = vars(self)
        # data = JsonResponse.format(self)  # type: dict
        for k, v in kwargs.items():
            if v is not None:
                data[k] = v
            else:
                data.pop(k, v)
        return data

    def to_json(self, **kwargs):
        data = JsonResponse.format(self, **kwargs)
        return data


class JsonResponse():
    DEFAULT_VERSION = "v2"
    DEFAULT_ERRNO = 40000  # type: int
    _version_enums = ["v0", "v1", "v2", "v3"]

    # DEFAULT_ERRNO = int(_env("PY_HTTP_DEFAULT_ERRNO", "40000"))

    @staticmethod
    def describe_status(code):
        status_enum = HTTP_STATUS_ENUMS_MAP.get(code, None)
        if status_enum is not None:
            return f"[{status_enum.name}:{code}] {status_enum.description}"
        return f"[???:{code}] invalid http status !!!"

    @classmethod
    def format(cls, err_or_res: Exception, **kwargs):
        if isinstance(err_or_res, Exception):
            if not isinstance(err_or_res, BaseApiError):
                err_or_res = BaseApiError(
                    msg=getattr(err_or_res, "msg", str(err_or_res)),
                    errno=getattr(err_or_res, "errno", cls.DEFAULT_ERRNO),
                    tracked_error=err_or_res,
                )
        func = getattr(cls, f"_format_{cls.DEFAULT_VERSION}")
        if not callable(func):
            func = cls._format_v2
        data = func(err_or_res)
        for k, v in kwargs.items():
            if v is not None:
                data[k] = v
            else:
                data.pop(k, v)
        return data

    @staticmethod
    def _format_v0(err):
        # version:0
        # response200: {result=$, errno=0}
        if not isinstance(err, BaseApiError):
            return dict(errno=0, result=err)
        return dict(
            errno=err.errno,
            msg=err.msg,
        )

    @staticmethod
    def _format_v1(err):
        # version:1
        # response200: {success=True, result=$}
        if not isinstance(err, BaseApiError):
            return dict(errno=0, success=True, result=err)
        return dict(
            errno=err.errno,
            success=False,
            message=err.msg,
        )

    @staticmethod
    def _format_v2(err):
        # version: 2
        # response200: {code=0, result=$, <request_id>, <error>}
        if not isinstance(err, BaseApiError):
            return dict(code=0, result=err, request_id=BaseApiError.new_request_id("r"))
        m = dict(
            code=err.errno,  # type: int
            error=f"[{err.__class__.__name__}] {err.msg}",  # type: str
            request_id=err.request_id,
        )
        if err.kwargs:
            m["error_info"] = err.kwargs
        return m

    @staticmethod
    def _format_v3(err):
        # version: 3
        # response200:  {errno=0, result=$, <request_id>}
        if not isinstance(err, BaseApiError):
            return dict(
                errno=0,
                result=err,
                result_type=type(err),
                request_id=BaseApiError.new_request_id("r")
            )
        return dict(
            errno=err.errno,
            error_msg=err.msg,
            error_kws=err.kwargs,
            result_type="ERROR:" + err.__class__.__name__,
            request_id=err.request_id,
        )
