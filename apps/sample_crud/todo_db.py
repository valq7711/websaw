import os

from websaw import DAL
from voodoodal import ModelBuilder

from .todo_model import TodoModel

_db = DAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)

# All magic goes here
@ModelBuilder(_db)
class db(TodoModel):
    pass

db.commit()
