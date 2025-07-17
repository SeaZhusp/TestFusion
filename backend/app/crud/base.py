import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, delete, update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select as SelectType
from sqlalchemy.sql.elements import BinaryExpression
from typing import Any, List, Union

from app.core.enums import DeleteStatus
from app.core.global_exc import CustomException


class BaseDal:
    ORDER_FIELD = ["desc", "descending"]

    def __init__(self, db: AsyncSession = None, model: Any = None, schema: Any = None):
        self.db = db
        self.model = model
        self.schema = schema

    async def get_data(self, data_id: int = None, v_return_none=False, v_schema=None, v_expire_all=False, **kwargs):
        if v_expire_all:
            self.db.expire_all()

        sql = await self.build_query(**kwargs)
        if data_id:
            sql = sql.where(self.model.id == data_id)

        result = await self.db.scalars(sql)
        data = result.unique().first() if kwargs.get("v_options") else result.first()

        if not data:
            if v_return_none:
                return None
            raise HTTPException(status_code=404, detail="未找到此数据")

        if v_schema:
            return await self.serialize(data, v_schema)
        else:
            return data

    async def get_datas(self, page=1, limit=10, v_return_count=False, v_return_scalars=False,
                        v_return_objs=False, v_schema=None, v_use_scalars=True, **kwargs):
        sql = await self.build_query(**kwargs)

        count = 0
        if v_return_count:
            count_sql = select(func.count()).select_from(sql.alias())
            count_result = await self.db.execute(count_sql)
            count = count_result.scalar()

        if limit:
            sql = sql.offset((page - 1) * limit).limit(limit)

        result = await self.execute_query(sql, use_scalars=v_use_scalars)

        if v_return_scalars:
            return (result, count) if v_return_count else result

        all_data = result.unique().all() if kwargs.get("v_options") else result.all()
        if v_return_objs:
            return (all_data, count) if v_return_count else all_data

        serialized = [await self.serialize(obj, v_schema) for obj in all_data]
        return (serialized, count) if v_return_count else serialized

    async def get_count(self, v_where: List[BinaryExpression] = None, **kwargs) -> int:
        sql = await self.build_query(v_start_sql=select(func.count(self.model.id)), v_where=v_where, **kwargs)
        result = await self.db.execute(sql)
        return result.scalar()

    async def create_data(self, data, v_schema=None, v_return_obj=False):
        obj = self.model(**(data if isinstance(data, dict) else data.model_dump()))
        await self.flush(obj)
        return await self.serialize(obj, v_schema, v_return_obj)

    async def create_datas(self, datas: List[dict]):
        await self.db.execute(insert(self.model), datas)
        await self.db.flush()

    async def put_data(self, data_id: int, data: Any, v_schema=None, v_return_obj=False):
        obj = await self.get_data(data_id)
        for key, value in jsonable_encoder(data).items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.serialize(obj, v_schema, v_return_obj)

    async def delete_datas(self, ids: List[int], v_soft=False, **kwargs):
        if v_soft:
            await self.db.execute(update(self.model).where(self.model.id.in_(ids)).values(
                delete_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_delete=True,
                **kwargs
            ))
        else:
            await self.db.execute(delete(self.model).where(self.model.id.in_(ids)))
        await self.db.flush()

    async def delete_datas_condition(self, v_where: List[BinaryExpression], v_soft=False, **kwargs):
        if v_soft:
            await self.db.execute(update(self.model).where(*v_where).values(
                delete_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                is_delete=True,
                **kwargs
            ))
        else:
            await self.db.execute(delete(self.model).where(*v_where))
        await self.db.flush()

    async def build_query(self, v_start_sql: SelectType = None, v_where=None, v_order=None, v_order_field=None,
                          v_select_from=None, v_join=None, v_outer_join=None, v_options=None, **kwargs):
        sql = v_start_sql or select(self.model).where(self.model.is_delete == DeleteStatus.NO.value)
        sql = self.add_relation(sql, v_select_from, v_join, v_outer_join, v_options)
        sql = self.add_filter_condition(sql, v_where, **kwargs)
        sql = self.add_order(sql, v_order, v_order_field)
        return sql

    def add_relation(self, sql: SelectType, v_select_from=None, v_join=None, v_outer_join=None, v_options=None):
        if v_select_from:
            sql = sql.select_from(*v_select_from)
        for joins, method in [(v_join, 'join'), (v_outer_join, 'outerjoin')]:
            if joins:
                for rel in joins:
                    target = getattr(self.model, rel[0]) if isinstance(rel[0], str) else rel[0]
                    sql = getattr(sql, method)(target, rel[1]) if len(rel) == 2 else getattr(sql, method)(target)
        if v_options:
            sql = sql.options(*v_options)
        return sql

    def add_order(self, sql: SelectType, v_order=None, v_order_field=None):
        if v_order_field:
            field = getattr(self.model, v_order_field)
            sql = sql.order_by(field.desc() if v_order in self.ORDER_FIELD else field)
        elif v_order in self.ORDER_FIELD:
            sql = sql.order_by(self.model.id.desc())
        return sql

    def add_filter_condition(self, sql: SelectType, v_where=None, **kwargs):
        if v_where:
            sql = sql.where(*v_where)
        conditions = self.__dict_filter(**kwargs)
        if conditions:
            sql = sql.where(*conditions)
        return sql

    def __dict_filter(self, **kwargs) -> List[BinaryExpression]:
        conditions = []
        for field, value in kwargs.items():
            if value is None or value == "":
                continue

            attr = getattr(self.model, field)

            if isinstance(value, tuple):
                if len(value) == 0 or value[1] in (None, ""):
                    continue  # 忽略无效操作或空值
                op, val = value[0], value[1]

                if op == "like":
                    conditions.append(attr.like(f"%{val}%"))
                elif op == "in":
                    if isinstance(val, list) and val:
                        conditions.append(attr.in_(val))
                elif op == "between" and isinstance(val, list) and len(val) == 2:
                    conditions.append(attr.between(val[0], val[1]))
                elif op == "!=":
                    conditions.append(attr != val)
                elif op == ">":
                    conditions.append(attr > val)
                elif op == ">=":
                    conditions.append(attr >= val)
                elif op == "<=":
                    conditions.append(attr <= val)
                elif op == "None":
                    conditions.append(attr.is_(None))
                elif op == "not None":
                    conditions.append(attr.isnot(None))
                elif op == "date":
                    conditions.append(func.date_format(attr, "%Y-%m-%d") == val)
                elif op == "month":
                    conditions.append(func.date_format(attr, "%Y-%m") == val)
                else:
                    raise CustomException("SQL查询语法错误")
            else:
                conditions.append(attr == value)

        return conditions

    async def execute_query(self, sql: SelectType, use_scalars=True):
        return await (self.db.scalars(sql) if use_scalars else self.db.execute(sql))

    async def serialize(self, obj: Any, v_schema=None, v_return_obj=False):
        if v_return_obj:
            return obj
        schema = v_schema or self.schema
        return schema.model_validate(obj).model_dump()

    async def flush(self, obj: Any = None):
        if obj:
            self.db.add(obj)
        await self.db.flush()
        if obj:
            await self.db.refresh(obj)
        return obj
