from datetime import datetime
from sqlalchemy import Table, Index, Integer, String, Column, Text, \
    DateTime, Boolean, PrimaryKeyConstraint, \
    UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Entity(Base):
    __tablename__ = 'entities'
    
    inn = Column(String(10), nullable=False, primary_key=True)
    ogrn = Column(String(13), nullable=False)
    kpp = Column(String(9), nullable=False)
    name = Column(String(500), nullable=False)
    short_name = Column(String(500), nullable=False)
    address = Column(String(500), nullable=False)
    # chief_position = Column(String(100), nullable=False)
    # chief = Column(String(500), nullable=False)
    reg_date = Column(String(10), nullable=False)

    def __init__(self, inn, ogrn, kpp, name, address) -> None:
        self.inn = inn
        self.ogrn = ogrn
        self.kpp = kpp
        self.name = name
        self.address = address

    def __repr__(self) -> str:
        return "{}, {}, {}, {}, {}, {}, {}".format(self.inn, self.ogrn, self.kpp, self.name, self.address, self.short_name, self.reg_date)


