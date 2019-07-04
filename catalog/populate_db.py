from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.entities import Base, Category, Item, User

engine = create_engine('postgresql://grader:grader@localhost:5432/catalog')
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


# Create dummy user
user_picture = "https://pbs.twimg.com/profile_images/2671170543/" \
    "18debd694829ed78203a5a36dd364160_400x400.png"
user1 = User(
    name="John Snow",
    username="john.snow@got.com",
    picture=user_picture)
user1.hash_password('12345678')
session.add(user1)
session.commit()

# Create categories
soccer = Category(name="Soccer", description="")
snowboarding = Category(name="Snowboarding", description="")
baseball = Category(name="Baseball", description="")
hockey = Category(name="Hockey", description="")
frisbee = Category(name="Frisbee", description="")

session.add(soccer)
session.add(snowboarding)
session.add(baseball)
session.add(hockey)
session.add(frisbee)
session.commit()

# Create Items
stick = Item(
    name="Stick",
    description="The Description",
    user=user1,
    category=hockey)
goggles = Item(
    name="Goggles",
    description="The Description",
    user=user1,
    category=snowboarding)
snowboard = Item(
    name="Snowboard",
    description="The Description",
    user=user1,
    category=snowboarding)
two_shinguards = Item(
    name="Two Shinguards",
    description="The Description",
    user=user1,
    category=soccer)
shinguards = Item(
    name="Shinguards",
    description="The Description",
    user=user1,
    category=soccer)
frisbee = Item(
    name="Frisbee",
    description="The Description",
    user=user1,
    category=frisbee)
bat = Item(
    name="Bat",
    description="The Description",
    user=user1,
    category=baseball)
jersey = Item(
    name="Jersey",
    description="The Description",
    user=user1,
    category=soccer)
soccer_cleats = Item(
    name="Soccer Cleats",
    description="The Description",
    user=user1,
    category=soccer)

session.add(stick)
session.add(goggles)
session.add(snowboard)
session.add(two_shinguards)
session.add(shinguards)
session.add(frisbee)
session.add(bat)
session.add(jersey)
session.add(soccer_cleats)
session.commit()

print "Data successfully added!"
