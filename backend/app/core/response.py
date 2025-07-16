from fastapi.responses import ORJSONResponse as Response


class SuccessResponse(Response):
    """
    成功响应
    """

    def __init__(self, data=None, msg="success", code=200, status=200, **kwargs):
        self.data = {
            "code": code,
            "message": msg,
            "data": data
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)


class ErrorResponse(Response):
    """
    失败响应
    """

    def __init__(self, msg=None, code=400, status=400, **kwargs):
        self.data = {
            "code": code,
            "message": msg,
            "data": []
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)
