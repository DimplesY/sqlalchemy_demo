#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：sqlalchemy_demo 
@File    ：main.py
@Author  ：DimplesY
@Date    ：2024/10/14 19:28 
"""
from sqlalchemy import Table, MetaData, insert, select, and_, or_, func, desc

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/demo", echo=True)
session_maker = sessionmaker(bind=engine)
session = session_maker()

meta_obj = MetaData()

user_table = Table(
    "user_account",
    meta_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(30)),
    Column("email", String(30), unique=True)
)

address_table = Table(
    "address",
    meta_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("address", String, nullable=False)
)


def create_tables():
    meta_obj.create_all(engine)


def insert_returning():
    select_stmt = select(user_table.c.id, user_table.c.name + "的地址")
    insert_stmt = insert(address_table).from_select(["user_id", "address"], select_stmt).returning(
        address_table.c.id,
        address_table.c.address
    )


def select_demo():
    stmt = select(user_table).where(and_(
        address_table.c.user_id == user_table.c.id,
        or_(user_table.c.name == "DimplesY", user_table.c.name == "test")
    ))
    return stmt


def func_test():
    select_stmt = select(func.count("*")).select_from(user_table).order_by(desc(user_table.c.id)).join(address_table,
                                                                                                       user_table.c.id == address_table.c.user_id)
    print(select_stmt)


if __name__ == '__main__':
    func_test()
