"""
pip install flask
"""
from pprint import pformat
from werkzeug.exceptions import HTTPException
from flask import (
    jsonify,
    session,
    request,
    has_request_context,
)
from py_http_errors._base import BaseApiError, JsonResponse


class FlaskApiError(BaseApiError, HTTPException):
    errno = 40000
    code = 400
    msg = "ApiError"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.code = self.status
        self.description = self._describe_status()

    def _gen_printable_item(self):
        if has_request_context():
            uid = session.get('user_id', '')
            u = session.get('username', '')
            yield f'{request.method} {request.full_path} {self.status} - {uid}:{u}:{self.request_id}'
            yield f'{request.endpoint} {request.view_args} '
            # yield f'[$Form] {pformat(request.form_json)}'
        yield f"[{self.__class__.__name__}] {self.errno}: {self.msg}"
        if self.kwargs:
            yield f'[kwargs] {pformat(self.kwargs, indent=2)}'

    def __str__(self):
        return "\n\t".join(map(str, self._gen_printable_item()))

    def get_response(self, environ=None):
        result = JsonResponse.format(self)
        return jsonify(result), self.status
