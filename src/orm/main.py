#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：sqlalchemy_demo 
@File    ：main.py
@Author  ：DimplesY
@Date    ：2024/10/14 18:51 
"""
from typing import List

from sqlalchemy import create_engine, Integer, String, ForeignKey, select, func
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, relationship, mapped_column

engine = create_engine("postgresql+psycopg2://postgres:123456@localhost:5432/demo", echo=True)
session_maker = sessionmaker(bind=engine)
session = session_maker()

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, nullable=True)
    email = mapped_column(String, nullable=False, unique=True)
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "user_address"
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    address = mapped_column(String, nullable=False)
    user: Mapped[User] = relationship(back_populates="addresses")


def create_tables():
    Base.metadata.create_all(engine)


def insert_returning():
    select_stmt = select(User.id, User.username + "的地址")

    insert_stmt = insert(Address).from_select([
        Address.user_id,
        Address.address
    ], select_stmt).returning(Address.id, Address.address)

    print(insert_stmt)



if __name__ == '__main__':
    pass
