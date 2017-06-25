#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item

engine = create_engine('postgresql://catalog:password@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

conn = engine.connect()


# Sports Category
category1 = Category(name="Sports", creator="admin")

session.add(category1)
session.commit()


item1 = Item(name="Football",
             description="Score touchdowns",
             creator="admin", category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Basketball",
             description="Shoot the ball in the hoop",
             creator="admin", category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Soccer",
             description="Kick the ball in the goal",
             creator="admin", category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Baseball",
             description="Hit the ball with a stick",
             creator="admin", category=category1)

session.add(item4)
session.commit()

item5 = Item(name="Rugby",
             description="The only real man sport",
             creator="admin", category=category1)

session.add(item5)
session.commit()

item6 = Item(name="Cricket",
             description="What even is this?",
             creator="admin", category=category1)

session.add(item6)
session.commit()

item7 = Item(name="Volleyball",
             description="Be tall, win",
             creator="admin", category=category1)

session.add(item7)
session.commit()

item8 = Item(name="Dodgeball",
             description="Aim low, injure everyone!",
             creator="admin", category=category1)

session.add(item8)
session.commit()


# Entertainment Category
category1 = Category(name="Entertainment", creator="admin")

session.add(category1)
session.commit()

# Video Games subcategory
category2 = Category(name="Video Games",
                     description="Interactive escape from reality",
                     parent_id=category1.id)

session.add(category2)
session.commit()

item1 = Item(name="Call of Duty",
             description="Get yelled at by 9 year olds",
             creator="admin", category=category2)

session.add(item1)
session.commit()

item2 = Item(name="Battlefield",
             description="Is this real life?",
             creator="admin", category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Skate",
             description="I'm a punk, I swear!",
             creator="admin", category=category2)

session.add(item3)
session.commit()

item4 = Item(name="Rocket League",
             description="Where'd the ball go?",
             creator="admin", category=category2)

session.add(item4)
session.commit()

item5 = Item(name="Watch Dogs",
             description="Hacker man!",
             creator="admin", category=category2)

session.add(item5)
session.commit()

item6 = Item(name="Assassin\'s Creed",
             description="Tallest building in the city? Lets jump!",
             creator="admin", category=category2)

session.add(item6)
session.commit()


# Movie subcategory
category2 = Category(name="Movies", parent_id=category1.id)

session.add(category2)
session.commit()


item1 = Item(name="Guardians of the Galaxy",
             description="I am groot.",
             creator="admin", category=category2)

session.add(item1)
session.commit()

item2 = Item(name="Harry Potter",
             description="You\'re a wizard, Harry!",
             creator="admin", category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Annabelle",
             description="So cheesy it\'s scary!",
             creator="admin", category=category2)

session.add(item3)
session.commit()

item4 = Item(name="Rubber",
             description="Terrorist Tire",
             creator="admin", category=category2)

session.add(item4)
session.commit()


# Category for Food
category1 = Category(name="Food")

session.add(category1)
session.commit()


item1 = Item(name="Pizza",
             description="If you don't like it, you\'re a communist",
             creator="admin", category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Soup",
             description="Feeling okay?",
             creator="admin", category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Salad",
             description="\"I'm healthy\"",
             creator="admin", category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Pasta",
             description="Mama mia, perfecto!",
             creator="admin", category=category1)

session.add(item4)
session.commit()

item5 = Item(name="Street Taco",
             description="Need I say more?",
             creator="admin", category=category1)

session.add(item5)
session.commit()


# Activities Category
category1 = Category(name="Activities")

session.add(category1)
session.commit()


item1 = Item(name="Mini Golf",
             description="Because golf is for old men",
             creator="admin", category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Water Park",
             description="Too hot in the sun, too cold in the water",
             creator="admin", category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Amusement Park",
             description="Weeeeee",
             creator="admin", category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Hiking",
             description="10 feet in: *Heaving*",
             creator="admin", category=category1)

session.add(item4)
session.commit()

item5 = Item(name="Running",
             description="Haha yeah right!",
             creator="admin", category=category1)

session.add(item5)
session.commit()

print "Added categories & items!"
