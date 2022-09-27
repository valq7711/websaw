import os
import ombott

from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture
from websaw.fixtures import XAuth
from websaw.fixtures.dbregistry import DBRegistry
from . import settings
from PIL import Image

from .auth_db import db

ombott.default_app().setup(dict(debug=True))

# Define our menus here

def resize_image(image_path):
    img = Image.open(image_path)
    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(image_path)


def cleanup_image(image_path):
    #total_path = os.path.join(settings.UPLOAD_PATH, image_path)
    try:
        os.remove(image_path, dir_fd=None)
    except:
        print('Could not find file to remove', image_path)


class GetNavbar(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        self.data.db = ctx.db
        self.data.user = ctx.current_user.user
            
        if self.data.user:
            ctx.env['default_template_context']['user'] = self.data.user['email']
            ctx.env['default_template_context']['buttons'] = [
                {'name':'Profile', 'href':ctx.URL('profile')},
                {'name':'Log Out', 'href':ctx.URL('logout')},
            ]
        else:
            ctx.env['default_template_context']['user'] = ''
            ctx.env['default_template_context']['buttons'] = [
                {'name':'Log In', 'href':ctx.URL('login')},
                {'name':'Register', 'href':ctx.URL('register')},
            ]

navbar=GetNavbar()

class Flash(Fixture):
    def take_off(self, ctx: DefaultContext):
        ...
        
    def set(self, ctx, message, _class=None):
        f_message = dict(message=message, _class=_class)
        session = ctx.session
        session['flash_message'] = f_message

flash = Flash()


class Auth(XAuth):
    def take_on(self, ctx: DefaultContext):
        self.data.ctx = ctx
        self.data.db = ctx.db
        self.data.session = ctx.session
        self.data.cuser = ctx.current_user
        self.data.user = self.data.cuser.user
        #self.data.flash = ctx.flash
        
    def user_by_login(self, login: str) -> dict:
        login = login.lower()
        db = self.data.ctx.db
        user = db(db.user.username == login).select().first()
        return user
        
    def user_for_session(self, user):
        suser = super().user_for_session(user)
        suser['email'] = user['email']
        suser['username'] = user['username']
        suser['first_name'] = user['first_name']
        suser['last_name'] = user['last_name']
        return suser

    def register(self, fields):
        db = self.data.ctx.db
        ret = db.user.insert(**fields)
        db.commit()
        return ret

    def update_profile(self, user_id, fields):
        db = self.data.ctx.db
        res = db.user(user_id).update_record(
            username = fields["username"],
            email = fields["email"],
            first_name = fields["first_name"],
            last_name = fields["last_name"],
        )
        db.commit()
        if res:
            self.store_user_in_session(res.as_dict())
            return res['id']
        else:
            return dict(message='Could not update profile', _class='danger')    

    def has_membership(self, role):
        user_id = self.user_id
        db = self.data.db
        belongs = db(db.auth_membership.user_id == user_id).select()
        for b in belongs:
            if db.auth_roles(b.role_id).role == role:
                return True
        return False

auth = Auth()

# extend default context with our fixture/s

class Context(DefaultContext):
    
    env={
        'default_template_context': dict(user = ''),
    }
    db = db
    auth = auth
    navbar = navbar
    flash = flash
    db_registry = DBRegistry()

ctxd = Context()

app = DefaultApp(ctxd, name=__package__ )
