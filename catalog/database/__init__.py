import sys
from sqlalchemy import create_engine
from entities import base, user, item, category
import query

engine = create_engine('sqlite:///database/catalog.db')
base.Base.metadata.create_all(engine)
