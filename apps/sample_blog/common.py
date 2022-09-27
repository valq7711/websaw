import os
from websaw.core import Fixture
from websaw import BaseContext, DefaultContext, XAuth
from websaw.fixtures.dbregistry import DBRegistry
from . import settings
from PIL import Image
from ..mixins import auth
from .blog_db import db
from .menus import menus

class GetNavbar(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        self.data.db = ctx.db
        self.data.user = ctx.current_user.user
            
        if self.data.user:
            ctx.env['default_template_context']['user'] = self.data.user['email']
            ctx.env['default_template_context']['buttons'] = [
                {'name': 'All Posts', 'href':ctx.URL('index')},
                {'name': 'New Post', 'href':ctx.URL('post', vars={'action':'new'})},
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

class GetUserMenus(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        navbar = ctx.navbar
        self.data.db = ctx.db
        self.data.user = ctx.current_user.user
        db = self.data.db
        role = ''
        member=None
        if self.data.user:
            user_id = self.data.user['id']
            member = db(db.membership.user_id == user_id).select().first()
            
        if not member:
            role = 'user'
        else:
            role = db.role(member.role_id).role
        if not role in ctx.env['menus']:
            ctx.env['default_template_context']['menu'] = []
        else:
            ctx.env['default_template_context']['menu'] = ctx.env['menus'][role]

menu=GetUserMenus()

# extend default context with our fixture
class Context(auth.Context, DefaultContext):
    env={
        'menus' : menus,
        'menu': [],
        'default_template_context': dict(user = ''),
        'default_template_context': dict(buttons = ''),
        'default_template_context': dict(menu = ''),
    }
    db = db
    db_registry = DBRegistry()
    menus = menu
    