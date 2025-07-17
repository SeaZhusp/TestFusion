from fastapi import Depends, Query

from app.core.dependencies.query import QueryParams, Paging


class UserParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            fullname: str | None = Query(None, title="姓名"),
            username: str | None = Query(None, title="账号"),
            status: int | None = Query(None, title="状态"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.fullname = ("like", fullname)
        self.username = ("like", username)
        self.status = status
        self.v_order = "desc"
        self.v_order_field = "id"
