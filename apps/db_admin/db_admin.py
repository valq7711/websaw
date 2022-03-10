import os
from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import Fixture
from .common import app, ctx_
from .models import auth_db
from .form_1 import Form, FormStyleBulma
import ombott
from .datatables_client import Grid
from pydal.validators import IS_NOT_EMPTY, IS_INT_IN_RANGE, IS_IN_SET, IS_IN_DB
from yatl.helpers import INPUT, H1, A, DIV, SPAN, XML
#from .datatables_server import *
from .datatables_utils import DtGui
dtgui=DtGui()

from pprint import pprint
import json

def b_fields(flds):
    f_str=''
    for f in flds:
        f_str += '&nbsp;<span class="tag tag-info">%s</span>' % f
    return f_str

@app.route('db_admin', method=['GET','POST'])
@app.use('db_admin.html')
def db_admin(ctx: ctx_):
    #user = auth.get_user()
    #print('session role is ', session.get('role', ''))
    #grps = groups.get(auth.get_user()['id'])
    #if not 'admin' in grps:
    #    redirect(URL('index'))
    db = None
    #print('Keys are ', ctx.db_reg.dbs_keys)
    #pprint(vars(ctx.auth))
    cdb = ctx.request.query.get('current_db', None)
    if not cdb and not ctx.db_reg.dbs_keys: ### so no database to use here ### 
        print('WE DONT HAVE ANY DBS. Decide what to do next')
    if cdb:
        db = ctx.ask(cdb)
    else:
        cdb = list(ctx.db_reg.dbs_keys)[0] ### get the first element of the set
        db = ctx.ask(cdb)        
    cols = [{ "data": "name" },{ "data": "fields" }]
    headers=['Table','Fields']
    recs = []
    for tbl in db.tables:
        tbls = {}
        flds = []
        for fld in db[tbl]:
            flds.append(fld.name)
        href = ctx.URL('table_admin', vars={"caller":"db_admin","cdb":cdb, "table":tbl})
        tbls["name"] = dtgui.get_admin_button('table', tbl, href)
        tbls["fields"] = b_fields(db[tbl].fields)
        recs.append(tbls)
    r = json.dumps(recs)
    recs = r
    return dict(recs=recs, hdrs=headers, cols=cols, dbs=ctx.db_reg.dbs_keys, level='admin')

@app.route('table_admin', method=['GET','POST'])
@app.use('datatables.html')
def table_admin(ctx: ctx_):
    #user = auth.get_user()
    #print('has membershitp', has_membership('admin'))
    
    #if user:
    #    if not 'admin' in groups.get(auth.get_user()['id']):
    #        redirect(URL('index'))
    #else:
    #    redirect(URL('index'))
    my_dict = ctx.request.query.decode()
    session = ctx.session
    cdb = my_dict.get('cdb', None) #ctx.ask(ctx.request.query.get('db', None)
    db = ctx.ask(cdb)
    session['orig_query']=''
    caller = my_dict.caller
    if not caller == 'table_admin' and caller:
        session['orig_caller'] = caller
    if caller:
       b_button = dtgui.get_dt_button('back', ctx.URL(my_dict['caller'], vars={"cdb":cdb,"table":my_dict.table}), "Back", 'Back')
    else:
        b_button = dtgui.get_dt_button('back', ctx.URL(session['orig_caller'], vars={"cdb":cdb,"table":my_dict.table}), "Back", 'Back')
    grid = Grid(ctx, cdb, db[my_dict.table], back=b_button)
    #fields= grid.get_fields()
    #f_form = s_form.search_form(db, my_dict.table, fields, session, T, 'table_admin')
    f_form=''
    return dict(grid = grid, level="admin", f_form=f_form) # user=user, groups=grps)
