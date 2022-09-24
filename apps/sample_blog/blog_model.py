import os
from websaw import Field, BaseContext
from websaw.core import Fixture
from voodoodal import Table, Field
from voodoodal.pydal_db_validators import is_in_db, is_not_in_db
from pydal.validators import IS_NOT_EMPTY
from pydal import DAL
import datetime

from . import settings

def get_time_stripped():
    fulltime = datetime.datetime.utcnow() 
    stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
    retval = stripped.replace("T"," ")
    return retval.replace("T"," ")

def get_user():
    return BaseContext.cctx().current_user.user.get('id', None)

class BlogModel(DAL):
    class post(Table):
        title = Field('string', requires=IS_NOT_EMPTY())
        content = Field('text', requires=IS_NOT_EMPTY())
        date_posted = Field('datetime', default=get_time_stripped, readable=False, writable=False)
        author = Field('reference user', requires=is_in_db('id', 'user.username'), default=get_user, readble=False, writable=False)
    