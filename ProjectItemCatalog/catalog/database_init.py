#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Base, Item, Category

engine = create_engine('sqlite:///catalog.db')
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


user_1 = User(
    name='Anthony',
    email='anthony.owen@gmail.com',
    picture=''
)
session.add(user_1)
session.commit()

category_1 = Category(
    name='Crypto Currency',
    user=user_1
)
session.add(category_1)
session.commit()

item_1 = Item(
    name='Bitcoin',
    description='Bitcoin (BTC) is a cryptocurrency, a form of electronic cash. It is a decentralized digital currency without a central bank or single administrator that can be sent from user to user on the peer-to-peer bitcoin network without the need for intermediaries.',
    category=category_1,
    user=user_1
)
session.add(item_1)
session.commit()

item_2 = Item(
    name='Litecoin',
    description='Litecoin (LTC) is a peer-to-peer cryptocurrency and open-source software project released under the MIT/X11 license.',
    category=category_1,
    user=user_1
)
session.add(item_2)
session.commit()


category_2 = Category(
    name='Fiat Currency',
    user=user_1
)
session.add(category_2)
session.commit()

item_3 = Item(
    name='USD',
    description='The United States dollar (sign: $; code: USD; also abbreviated US$ and referred to as the dollar, U.S. dollar, or American dollar) is the official currency of the United States and its territories per the United States Constitution since 1792.',
    category=category_2,
    user=user_1
)
session.add(item_3)
session.commit()

item_4 = Item(
    name='AUD',
    description='The Australian dollar (sign: $; code: AUD) is the currency of Australia (including its external territories Christmas Island, Cocos (Keeling) Islands, and Norfolk Island), and of three independent Pacific Island states, specifically Kiribati, Nauru, and Tuvalu.',
    category=category_2,
    user=user_1
)
session.add(item_4)
session.commit()

print "added menu items!"
