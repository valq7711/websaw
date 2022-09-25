import os

from distutils import errors
from multiprocessing.context import BaseContext
from pydal import Field
from websaw import DefaultApp, DefaultContext, BaseContext, Reloader, XAuth
from websaw.core import Fixture, redirect
from websaw.fixtures import Env
import ombott

from . import blog_templates as ut

ombott.default_app().setup(dict(debug=True))

from .. common.common_utils import SQLForm

from .common import Context

from ..mixins import auth
ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

# use mixin(s)
app.mixin(auth.app)

    
@app.route('post', method=['GET', 'POST'])
@app.use(ctxd.navbar, ctxd.menus, ut.post_template )
def post(ctx):
    user = ctx.auth.user
    flash = ctx.flash
    db = ctx.db
    my_dict = ctx.request.query.decode()
    action = my_dict.get('action', None)
    
    form = SQLForm(db.post)
    
    if not action:
        flash.set(ctx, 'You need to select an action for your Posts', 'warning')
        redirect(ctx.URL('index'))
    
    if not user:
        flash.set(ctx, 'You need to be logged in to make changed or delete your posts', 'warning')
        redirect(ctx.URL('login'))
    if action == 'new': #new post
        if form.process(ctx, db, db.post, None).accepted:
            if ctx.request.method == 'POST':
                flash.set(ctx, 'Congratulation you have successfully added a new post', 'success')
                redirect(ctx.URL('index'))
    
    if action == 'update':
        pid = my_dict.get('pid', None)
        if not pid:
            flash.set(ctx, 'You are trying to update an invalid post id', 'warning')
            redirect(ctx.URL('index'))
        print('PID is ', pid, 'User', user)
        
        post = db(db.post.id == pid).select().first()
        print('Post is ', post)
        if form.process(ctx, db, db.post, post).accepted:
            if ctx.request.method == 'POST':
                flash.set(ctx, 'Congratulations. You have updated your Post', 'success')
                redirect(ctx.URL('index'))
    
    if action == 'delete':
        pid = my_dict.get('pid', None)
        if not pid:
            flash.set(ctx,'You cannot delete that record we are logging you now', 'danger')
            redirect(ctx.URL('index'))
        post = db.post(pid)
        if post is None or post.author != user['id']:
            flash.set(ctx, 'You are not authorized to delete this record.', 'danger')
            redirect(ctx.URL("index"))
        db(db.post.id == pid).delete()
        db.commit()
        flash.set(ctx,'Congratulations. You have deleted your Post', 'success')
        redirect(ctx.URL("index"))

    return dict(form_options = form.get_options())   


@app.route('index')
@app.use(ctxd.navbar, ctxd.menus, ut.index_template)  # note there is no session, but it used!

def index(ctx: Context):
    
    flash = ctx.flash   # we are using the flash component form the auth mixin 
    session = ctx.session
    flash_message = session.get('flash_message', {})
    my_dict = ctx.request.query.decode()
    db = ctx.ask('db')
    
    posts = None
    if my_dict and my_dict.get('filter_by', None): 
        posts = db(db.post.author == my_dict.uid).select(
            left=db.post.on(db.post.author == db.profile.user_id), orderby=~db.post.date_posted
        )
    else:
        posts = db(db.post).select(
            left=db.post.on(db.post.author == db.profile.user_id), orderby=~db.post.date_posted
        )
    if not posts:
        flash.set(ctx, 'There are no posts yet on this system. Why not Login to create one', 'info')
    return dict(form_options = {'posts': posts, 'flash': flash_message})   
