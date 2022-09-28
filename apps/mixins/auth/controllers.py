import os
import json

from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import Fixture
import ombott
from pydal import Field

from .auth_db import db
from . import utemplates as ut
from . import auth_templates as at
from .upytl_form import SQLForm


ombott.default_app().setup(dict(debug=True))

from .common import Context, resize_image, cleanup_image

ctxd = Context()
app = DefaultApp(ctxd, config=dict(group_name='websaw_apps_group_one'), name=__package__)

@app.route('login', method=['GET', 'POST'])
@app.use(ctxd.navbar, at.login_template )

def login(ctx):
    db = ctx.ask('db')
    session = ctx.session
    flash = ctx.flash
    
    # We need to use a list of fields here as the password field is readonly in the db
    # this means that we have to do all post processing ourselves

    field_list = [(Field('username')), (Field('password', 'password'))]
    
    form = SQLForm(field_list)
    if form.process(ctx, db, db.user, None).accepted:
        if ctx.request.method == 'POST':
            user, autherr = ctx.auth.login(form.vars['username'], form.vars['password'] )
            if user:
                flash.set(ctx, 'Welcome %s %s you are welcome here' % (user['first_name'], user['last_name']), 'success')
                redirect(ctx.URL('index'))
            else:
                flash.set(ctx, 'Hey %s your credentials are INVALID. Please use the correct credentials or contact your administrator' % (form.vars['username']), 'danger')
                redirect(ctx.URL('login')) 
        else:
            return dict(form_options = form.get_options())
    else:
        flash.set(ctx, 'Form was not accepted. Please check with your admin', 'danger')
    return dict(form_options = form.get_options())
    

@app.route('register', method=['GET', 'POST'])
@app.use(ctxd.navbar, at.register_template)
def register(ctx: Context):
    db = ctx.ask('db')
    flash = ctx.flash
    
    # Again we need to get a list of fields as most fields in user file are readonly
    # Also we need to check that the same password is entered twide for confirm

    field_list = [field for field in db.user if not field.type == "id" and field.writable and not field.name =="is_blocked"] + [
        (Field('password', 'password')), (Field('password_again', 'password'))]
    form = SQLForm(field_list)
    if form.process(ctx, db, field_list, None).accepted:
        if ctx.request.method == 'POST':
            if form.vars['password'] == form.vars['password_again']:
                form.vars['password'] = ctx.auth.crypt(form.vars['password']) # crypt it here 
                res = ctx.auth.register(form.vars)
                if res: 
                    flash.set(ctx, 'Registration successfull', 'success')
                    redirect(ctx.URL('login'))
                else:
                    flash.set(ctx, 'Registration failed. Please check input and try again', 'danger')
            else:
                flash.set(ctx, 'Passwords do not match. Please type carefully', 'warning')          
    
    elif form.errors:
        flash.set(ctx, 'Form has errors  %s' % json.dumps(form.errors), 'danger')

    return dict(form_options = form.get_options())   

@app.route('logout', method=['GET', 'POST'])
def logout(ctx: Context):
    flash = ctx.flash
    user = ctx.auth.user
    if not user:
        message = 'Please log in to access this app'
    else:
        message = 'Hey %s you have just logged out .. see you soon' % user['email']    
    ctx.auth.logout()
    flash.set(ctx, message, 'info')
    redirect(ctx.URL('index'))

@app.route('profile', method=['GET', 'POST'])
@app.use(ctxd.navbar, at.profile_template)
def profile(ctx: Context):
    user = ctx.auth.user
    db = ctx.ask('db')
    icon = None
    flash = ctx.flash
    i_path = ctx['folder']+'/static/images/'
    db.profile.image.uploadfolder = i_path
    db.profile.image.download_url = i_path
    if not user:
        redirect(ctx.URL('login'))
    
    # Get all the required fields out of the 2 tables to display them: Username, Email, First/Last name
    # and also image from profile table
    
    field_list = [field for field in db.user if not field.type == "id" and field.writable and field.name!='is_blocked'] + [
        field for field in db.profile if not field.type == "id" and field.writable
    ]
    if ctx.request.method == 'GET':
        form = SQLForm(field_list)
        if form(ctx.request.json or ctx.request.POST, record_id = user['id']).accepted:   
            profile = db.user(user['id']).profile.select().first()
            if not profile:

                # If for some reason we dont have a default profile for this user just add one
                
                db.profile.insert(user=ctx.auth.user['id'], image='default.jpeg')
            profile = db.user(user['id']).profile.select().first()
            icon = f"static/images/{profile.image}"
            
            # Append the user profile icon to the dict so it prepopulates it with current data
            
            user.update({"image": profile.image})

            form.vars.update(user)
        else:
            flash.set(ctx, 'From was not accepted', 'warning')
    else: 

        # can only be a POST as we dont allow anything else

        form = SQLForm(field_list)
        
        #  When passing in a list of fields we need to take care of the processing ourselves
        
        if form(ctx.request.json or ctx.request.POST, record_id = user['id']).accepted:   
            if not isinstance(form.vars['image'], bytes): # We have selected a new image
                form.upload() 
                
                # so lets upload the image first

                profile = db.user(user['id']).profile.select().first()
                icon = f'static/images/{profile.image}'
                if profile.image == 'default.jpg':
                    flash.set(ctx, 'Sucsesfully updated your profile information', 'success')
                    form.update(db.profile, record_id = profile.id, del_files = False)
                
                    #  We DONT want to delete the default
                
                else:
                    form.update(db.profile, record_id = profile.id, del_files = True)
                    flash.set(ctx, 'Thanks for updating your Profile Image. Looking good', 'success')
                db.commit()
                
                # reread the profile table after updating
                
                profile = db.user(user['id']).profile.select().first()
                ipath = ctx['folder']+'/static/images/'+profile.image
                resize_image(ipath)
                
                # update the session with new information
                
                res = ctx.auth.update_profile(user['id'], form.vars)
                redirect(ctx.URL('profile'))
            else:        
                new_rec = form.update(db.user, record_id = user['id'])
                db.commit()
                
                res = ctx.auth.update_profile(user['id'], form.vars)
                profile = db.user(user['id']).profile.select().first()
                icon = f"static/images/{profile.image}"
                
                flash.set(ctx, 'Congratulations. You have successfully updated your profile. Looking good!!', 'success')
                redirect(ctx.URL("profile"))
        else:
            profile = db.user(user['id']).profile.select().first()
            icon = f"static/images/{profile.image}"
            
    return dict(form_options = form.get_options(), icon=icon)


@app.route('api/login')
def login(ctx: Context):
    q = ctx.request.query
    user, autherr = ctx.auth.login(q.login, q.pw)
    if user:
        redirect(ctx.URL('private'))
    return autherr.as_dict()


@app.route('api/logout')
def logout(ctx: Context):
    user = ctx.auth.user or dict(name="Guest")
    ctx.auth.logout()
    return f"Byе {user['name']}!"


@app.route('api/private')
@app.use(ctxd.auth_guard)
def private(ctx: Context):
    return dict(user_in_session=ctx.auth_guard.user)

#http://127.0.0.1:8000/xauth/login?login=tom&pw=tom_pass    #OK
#http://127.0.0.1:8000/xauth/login?login=kevin&pw=tom_pass  #401
#http://127.0.0.1:8000/xauth/login?login=john&pw=john_pass  #403
