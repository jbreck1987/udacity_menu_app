import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Restaurant(Base):

    # Set name of DB table associated
    # with this ORM class
    __tablename__ = 'restaurant'

    # Create mappings (table columns)
    Id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class MenuItem(Base):

    # Set name of DB table associated
    # with this ORM class
    __tablename__ = 'menu_item'

    # Create mappings (table columns)
    name = Column(String(80), nullable=False)
    Id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.Id'))
    restaurant = relationship(Restaurant)


# END OF FILE
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
