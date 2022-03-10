import os
from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import Fixture
from .models import auth_db
from .form_1 import Form, FormStyleBulma
import ombott
from .common import app, ctx_
from pprint import pprint

@app.route('login', method=['GET', 'POST'])
@app.use('index.html')
def login(ctx: ctx_):
    q = ctx.request.query
    db = ctx.auth_db
    form=Form(db.auth_user, formstyle=FormStyleBulma)
    grid = db(db.auth_user).select()

    return dict(form=form, grid=grid)
    #rows = db(db.auth_user).select()
    #return rows.as_dict()
    

@app.route('logout')
def logout(ctx: ctx_):
    user = ctx.auth.user or dict(name="Guest")
    ctx.auth.logout()
    return f"Byе {user['name']}!"


@app.route('private')
@app.use(ctx_.auth_guard)
def private(ctx: ctx_):
    return dict(user_in_session=ctx.auth_guard.user)

#http://127.0.0.1:8000/xauth/login?login=tom&pw=tom_pass    #OK
#http://127.0.0.1:8000/xauth/login?login=kevin&pw=tom_pass  #401
#http://127.0.0.1:8000/xauth/login?login=john&pw=john_pass  #403
