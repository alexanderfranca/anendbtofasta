from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

protein_ecs   = Table(
                     'protein_ecs',
                     Base.metadata,
                     Column('protein_id', Integer, ForeignKey('proteins.id')),
                     Column('ec_id', Integer, ForeignKey('ecs.id')),
                   )

