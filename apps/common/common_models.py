import os
from websaw import DAL, Field
from websaw.core import Fixture
from voodoodal import Table, Field
from pydal.validators import (IS_NOT_EMPTY, 
                              CRYPT,
                              IS_EMAIL,
                              IS_IN_DB,
                              IS_NOT_IN_DB
)



class AuthModel(DAL):
    class user(Table):
        username = Field('string', label='User Name', required=True, unique=True)
        first_name= Field('string', requires=IS_NOT_EMPTY(), label='First Name')
        last_name= Field('string', requires=IS_NOT_EMPTY(), label='Surname')
        email = Field('string', label='Email', unique=True)
        sso_id = Field('string', readable=False, writable=False)
        action_token = Field('string', readable=False, writable=False)
        last_password_change= Field('datetime', default=None, readable=False, writable=False)
        password = Field('password', requires=CRYPT(), readable=False, writable=False, label='Password')
        is_blocked = Field('boolean', default=False)
        format='%(email)s'
        singular = 'Auth User'
        plural = 'Auth Users'
        
        def after_insert(s, args):
            print('After_insert', s , args)
            db = s._table._db
            user_id = int(args)
            profile = db.user(user_id).profile.select().first()
            if not profile:
                profile = db.profile.insert(user_id=user_id)

    class role(Table):
        role = Field()
        desc=Field()
        format='%(desc)s'
        singular = 'Role'
        plural = 'Roles'
    
    class membership(Table):
        user_id = Field('reference user')
        role_id = Field('reference role')
        singular = 'Auth Membership'
        plural = 'Auth Memberships'

    class profile(Table):
        user_id = Field('reference user', readable=False, writable=False)
        image = Field('upload', default="default.jpg", label='Profile Image')

    @classmethod
    def on_define_model(cls, db: DAL, extras: dict):
        ## Postprocessing hook.
        #print('ON DEFINE MODEL', db, extras)
        db.user.username.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db,'user.username')]
        db.user.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, 'user.email')]
        db.membership.user_id.requires = IS_IN_DB(db,'user.id', 'user.email')
        db.membership.role_id.requires = IS_IN_DB(db,'role.id', 'role.desc')
        db.profile.user_id.requires = IS_IN_DB(db, 'user.id', 'user.email')
    # special hooks
    def on_action(tbl, hook, *args):
        """Convenient common hook for all before/after_insert/update/delete actions."""
        print('on_action', tbl, hook, args)
