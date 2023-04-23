from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import declarative_base
# from database import db_session, init_db

Base = declarative_base()
# Base.query = db_session.query_property()


class PlayerScore(Base):
    __tablename__ = "playerscore"

    id = Column(BigInteger, primary_key=True,
                unique=True, autoincrement=False)
    user_name = Column(String)
    score = Column(BigInteger, default=0)


class Specialization(Base):
    __tablename__ = "Специальности 🌐"

    id = Column(
        "Идентификатор специальности",
        BigInteger,
        primary_key=True,
        unique=True,
        autoincrement=True)
    code = Column("Код специальности", String)
    name = Column("Название специальности", String)
    time_education = Column("Срок обучения", String)
    education_ways = Column("Форма обучения", String)
    # specializations_education_objects = relationship(
    #     "SpecializationEducationObject")


class SpecializationEducationObject(Base):
    __tablename__ = "Предметы специальности"

    id = Column(BigInteger, primary_key=True,
                unique=True, autoincrement=False)
    code = Column("Код предмета специальности", String)
    name = Column("Название предмета специальности", String)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
