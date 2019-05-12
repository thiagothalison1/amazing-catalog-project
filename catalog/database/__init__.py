import sys
from sqlalchemy import create_engine
from entities import base, user, item, category
import query

engine = create_engine('sqlite:///database/catalog.db',
                       connect_args={'check_same_thread': False})
query.init(engine)
base.Base.metadata.create_all(engine)
