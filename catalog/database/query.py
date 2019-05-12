from sqlalchemy.orm import sessionmaker
from entities import Base, Category, Item, User
from sqlalchemy import desc

# Global variable that holds the session with the database.
# It is used for CRUD operations on the database.
session = None


# Database query session inititalization
def init(engine):
    global session
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()


def get_user(username):
    user = session.query(User).filter_by(username=username).first()
    return user


# There are two ways for creating a new user on the system.
# Google profile information: When the user Sign Up with google credentials.
# System SIgn Up: User inserts some information on a form.
# Note: Today the picture url is supported only for the google sign up.
def create_user(user_info, is_sign_up):
    if is_sign_up:
        new_user = User(name=user_info['name'], username=user_info['username'])
        new_user.hash_password(user_info['password'])
    else:
        new_user = User(
            name=user_info['name'],
            username=user_info['username'],
            picture=user_info['picture'])
    session.add(new_user)
    session.commit()
    return get_user(user_info['username'])


def get_categories():
    categories = session.query(Category).all()
    return categories


def get_category(category_id):
    category = session.query(Category).filter(Category.id == category_id).one()
    return category


def get_category_items(category_id):
    items = session.query(Item).filter(Item.category_id == category_id).all()
    return items


def add_category(category_name, category_desc):
    new_category = Category(name=category_name, description=category_desc)
    session.add(new_category)
    session.commit()


def get_latest_items():
    latest_items = session.query(
        Item,
        Category.name).join(Category).filter(
        Item.category_id == Category.id).order_by(
            desc(
                Item.created_at)).limit(5).all()
    return latest_items


def add_item(item_name, item_desc, category_id, user_id):
    user = session.query(User).filter(User.id == user_id).one()
    new_item = Item(
        name=item_name,
        description=item_desc,
        category_id=category_id,
        user=user)
    session.add(new_item)
    session.commit()


def get_item(item_id):
    item = session.query(Item).filter(Item.id == item_id).one()
    return item


def edit_item(item_name, item_desc, item_id):
    item = get_item(item_id)
    item.name = item_name
    item.description = item_desc
    session.add(item)
    session.commit()


def delete_item(item_id):
    item = get_item(item_id)
    session.delete(item)
    session.commit()
