import os
from websaw import DAL, Field, BaseContext
from voodoodal import Table, Field
from voodoodal.pydal_db_validators import is_in_db, is_not_in_db
from pydal.validators import IS_NOT_EMPTY

def get_user():
    return BaseContext.cctx().current_user.user.get('id', None)

class AppModel(DAL):
    class owner(Table):
        name = Field('string', requires=IS_NOT_EMPTY())
        occupation = Field('string', requires=IS_NOT_EMPTY())
        notes = Field('text')
        format='%(name)s'
        singular='Owner'
        plural = 'Owners'

    class thing(Table):
        name = Field('string', requires=IS_NOT_EMPTY())
        description = Field('text')
        owner = Field('reference owner', requires=is_in_db('owner', 'id', 'owner.name'))    
        format='%(name)s'
        singular='Thing'
        plural = 'Things'
