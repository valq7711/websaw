import os
from websaw import DAL, Field
from pydal.validators import *
import uuid

class myDAL(DAL):
    def app_mounted(self, ctx):
        db_reg = ctx.ask('db_reg')
        if db_reg:
            self_key = ctx.get_or_make_fixture_key(self)
            db_reg.dbs_keys.add(self_key)

# define database and tables
auth_db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
auth_db.define_table(
    "auth_user",
    Field("username"),
    Field('email'),
    Field('password', 'password'),
    format='%(email)s'
)
auth_db.auth_user._singular = 'Auth User'
auth_db.auth_user._plural = 'Auth Users'

auth_db.define_table(
    "auth_group",
    Field("group"),
    format='%(group)s'
)
auth_db.auth_group._singular = 'Auth Group'
auth_db.auth_group._plural = 'Auth Groups'

auth_db.define_table(
    "group_users",
    Field("group_id", 'reference auth_group',
           requires=IS_IN_DB(auth_db, 'auth_group.id', 'auth_group.group' ) ),
    Field("user_id", 'reference auth_user',
          requires=IS_IN_DB(auth_db, 'auth_user.id', 'auth_user.email')),       
    format='%(group_id)s'
)
auth_db.group_users._singular = 'Group Users'
auth_db.group_users._plural = 'Group Users'

auth_db.commit()

db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
db.define_table(
    "owner",
    Field('user_id'),
    Field('name')
)
db.owner._singular = 'Owner'
db.owner._plural = 'Owners'

db.define_table(
    "things",
    Field('thing_id'),
    Field('name')
)
db.things._singular = 'Thing'
db.things._plural = 'Things'

db.commit()

another_db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
another_db.define_table(
    "another_owner",
    Field('user_id'),
    Field('name')
)
another_db.another_owner._singular = 'Owner'
another_db.another_owner._plural = 'Owners'

another_db.define_table(
    "another_things",
    Field('thing_id'),
    Field('name')
)
another_db.another_things._singular = 'Thing'
another_db.another_things._plural = 'Things'

another_db.commit()
