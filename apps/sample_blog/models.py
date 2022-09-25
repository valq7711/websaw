import os
from websaw import DAL, Field, BaseContext
from pydal.validators import *
import datetime
from . import settings

def get_time():
    fulltime = datetime.datetime.utcnow() 
    stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
    retval = stripped.replace("T"," ")
    return retval.replace("T"," ")

def get_user():
    return BaseContext.cctx().current_user.user.get('id', None)


def get_download_url(picture):
    return f"static/images/{picture}"

class myDAL(DAL):
    def app_mounted(self, ctx):
        db_reg = ctx.ask('db_reg')
        if db_reg:
            self_key = ctx.get_or_make_fixture_key(self)
            db_reg.dbs_keys.add(self_key)

db = myDAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)
db.define_table("auth_user",
    Field("username", requires=[IS_NOT_EMPTY(), IS_NOT_IN_DB(db, "auth_user.username")],
        unique=True, label='Username'
    ),
    Field("first_name", requires=IS_NOT_EMPTY(), label='First Name'),
    Field("last_name",  requires=IS_NOT_EMPTY(), label='Last Name' ),
    Field("last_password_change", "datetime", default=None, readable=False, writable=False),
    Field("email", requires=(IS_EMAIL(), IS_NOT_IN_DB(db, "auth_user.email")),
        unique=True, label='Email'),
    Field("password", "password", requires=CRYPT(),
        readable=False, writable=False, label='Password'),
    Field("past_passwords_hash", "list:string", writable=False, readable=False),
    Field('is_blocked', 'boolean', default=False),
    format='%(email)s'
)
db.auth_user._singular = 'Auth User'
db.auth_user._plural = 'Auth Users'

db.define_table('auth_roles',
                Field('role'),
                Field('description'),
                format='%(description)s')
db.auth_roles._singular = 'Auth Role'
db.auth_roles._plural = 'Auth Roles'

db.define_table('auth_membership',
    Field('user_id', 'reference auth_user', requires= IS_IN_DB(db, 'auth_user.id', 'auth_user.email')),
    Field('role_id', 'reference auth_roles'))
db.auth_membership._singular = 'Auth Membership'
db.auth_membership._plural = 'Auth Memberships'

db.define_table(
    "profile",
    Field("user", "reference auth_user", readable=False, writable=False),
    Field("image","upload",
        default="default.jpg",
        uploadfolder=settings.UPLOAD_PATH,
        download_url=get_download_url, label="Profile Picture"),
    )

def register_profile(field_values, user_id):
    profile = db.auth_user(user_id).profile.select().first()
    if not profile:
        profile = db.profile.insert(user=user_id)

db.auth_user._after_insert.append(register_profile)

db.define_table(
    "post",
    Field("title", "string", requires=IS_NOT_EMPTY()),
    Field("content", "text", requires=IS_NOT_EMPTY()),
    Field("date_posted", "datetime", default=get_time, readable=False, writable=False),
    Field(
        "author",
        "reference auth_user",
        default=get_user,
        readable=False,
        writable=False,
    ),
)

db.define_table(
    "test",
    Field("title", "string", requires=IS_NOT_EMPTY()),
    Field("content", "text", requires=IS_NOT_EMPTY()),
    Field("date_posted", "datetime", default=get_time, readable=False, writable=False),
    Field("chreckbox", "boolean", widget="Checkbox"),
    Field("radio", "boolean", widget="Radio")
    
)


db.commit()