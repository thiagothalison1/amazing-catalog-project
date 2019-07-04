import sys
from sqlalchemy import create_engine
from entities import base, user, item, category
import query

engine = create_engine('postgresql://grader:grader@localhost:5432/catalog')
query.init(engine)
base.Base.metadata.create_all(engine)
