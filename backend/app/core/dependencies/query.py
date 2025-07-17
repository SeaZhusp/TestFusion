import copy

__all__ = ["Paging", "QueryParams"]


class QueryParams:

    def __init__(self, params=None):
        if params:
            self.page = params.page
            self.limit = params.limit
            self.v_order = params.v_order
            self.v_order_field = params.v_order_field

    def dict(self, exclude: list[str] = None) -> dict:
        result = copy.deepcopy(self.__dict__)
        if exclude:
            for item in exclude:
                try:
                    del result[item]
                except KeyError:
                    pass
        return result


class Paging(QueryParams):
    """
    列表分页
    """

    def __init__(self, page: int = 1, limit: int = 10, v_order_field: str = None, v_order: str = None):
        super().__init__()
        self.page = page
        self.limit = limit
        self.v_order = v_order
        self.v_order_field = v_order_field
