#!/usr/bin/env python

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    ''' Category Class - extends declarative base
        Class used to define category table in database

        @Column id - unique id of the category
        @Column name - name of the category
        @Column description - optional description of the category
        @Column creator - creator of the category
        @Column parent_id - id of super category if category
                            is a subcategory
        @relationship parent - Category class if has parent
    '''
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    description = Column(String(250), nullable=True)
    creator = Column(String(250))
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    parent = relationship("Category")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'creator': self.creator,
            'id': self.id,
            'parent_id': self.parent_id
        }


class Item(Base):
    ''' Item Class - extends declarative base
        Class used to define item table in database

        @Column id - unique id of the item
        @Column name - name of the item
        @Column description - optional description of the item
        @Column creator - creator of the item
        @Column category_id - id of category item is in
        @relationship category - Category class
    '''
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False, unique=True)
    description = Column(String(250))
    creator = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'creator': self.creator,
            'id': self.id,
            'category_id': self.category_id
        }


engine = create_engine('postgresql://catalog:password@localhost/catalog')


Base.metadata.create_all(engine)
