from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture, redirect
from websaw.fixtures import Env, XAuth
from websaw.fixtures.dbregistry import DBRegistry
import ombott

from . import dbadmin_templates as dat
from . import settings

ombott.default_app().setup(dict(debug=True))

from ... common.common_utils import SQLForm
from ... common.common_utils import SQLGrid
from ... common.common_fixtures import GetNavbar

from ..  import auth
import json

class GetUserMenus(XAuth):
    
    def take_on(self, ctx:DefaultContext):
        
        user=[dict(label='User Menu', href=ctx.URL('db_admin'))]
        admin=[dict(label='Admin Menu', href=ctx.URL('db_admin'))]
        
        ctx.env['menus']['user']=user
        ctx.env['menus']['admin']=admin
        
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
            ctx.env['default_template_context']['menu'] = ctx.env['menus']['user']
        else:
            ctx.env['default_template_context']['menu'] = ctx.env['menus'][role]

menu=GetUserMenus()
    

# extend default context with our fixture

class Context(auth.Context, DefaultContext):
    env={
        'menus' : {},
        'default_template_context': dict(user = ''),
        'default_template_context': dict(buttons = ''),
        'default_template_context': dict(menu = ''),
    }
    menu = menu
    db_registry = DBRegistry()

ctxd = Context()
app = DefaultApp(ctxd, name=__package__)

app.mixin(auth.app)

def b_fields(flds):
    f_str=''
    for f in flds:
        f_str += '&nbsp;<span class="tag tag-info">%s</span>' % f
    return f_str

@app.route('db_admin', method=['GET','POST'])
@app.use(ctxd.navbar, dat.dbadmin_template)
def db_admin(ctx: Context):
    user = ctx.auth.user
    flash = ctx.flash
    name = 'db_admin'
    menu = ctx.menu
    db = None
    cdb = None
    dbs = list(ctx.db_registry.db_keys  )
    ctx.session['dbs'] = dbs
    
    if len(dbs) > 1:
        # we should promt user to choose the db to work on here 
        print('we have a number of dbs we should choose one here')
    else:
        ctx.session['cdb'] = dbs[0]
    
    if not user:
        flash.set(ctx,'You need to be logged in in order to access this site', 'danger')
        redirect(ctx.URL('login'))
    
    ## once we have set up the roles and have an admin user we can uncomment this !!
    #if not ctx.auth.has_membership('admin'):
    #    flash.set(ctx, 'You do NOT have Admin access rights !!!', 'danger')
    
    if not cdb and not ctx.db_registry.db_keys: ### so no database to use here ### 
        flash.set('There are no databases to administor. Please check your connections', 'danger')
    if cdb:
        db = ctx.ask(cdb)
    else:
        cdb = list(ctx.db_registry.db_keys)[0] ### get the first element of the set
        db = ctx.ask(cdb)        
    cols = [{ "data": "name" },{ "data": "fields" }]
    headers=['Table','Fields']
    recs = []

    for tbl in db.tables:
        tbls = {}
        flds = []
        for fld in db[tbl]:
            fld.readable = fld.writable = True
            flds.append(fld.name)
        href = ctx.URL('table_admin', vars={"caller":"db_admin","cdb":cdb, "table":tbl})
        tbls["name"] = '<a class="tag is-link" href="%s"><i class="fas fa-list text-info"></i>&nbsp;%s</a>' %(
            ctx.URL('table_admin', vars=dict(caller='db_admin', cdb=cdb, table=tbl)), tbl)
        tbls["fields"] = b_fields(db[tbl].fields)
        recs.append(tbls)
    r = json.dumps(recs)
    recs = r
    grid_buttons = []
    dumpdb_button = '<a href="%s"><i class="%s"></i>&nbsp;%s</a>' % (ctx.URL('dump_db', vars={'cdb':cdb}),
                                                                     'fas fa-download', 
                                                                     'Dump DB to CSV')
    upload_db_button = '<a href="%s"><i class="%s"></i>&nbsp;%s</a>' %(ctx.URL('upload_db', vars={'cdb':cdb}),
                                                                       'fas fa-upload',
                                                                        'Restore DB from CSV')
    grid_buttons.append(upload_db_button)
    grid_buttons.append(dumpdb_button)
    
    return dict(grid_options = {'name':name, 'headers': headers, 'columns':cols, 'data':recs, 'grid_buttons':grid_buttons})   

@app.route('dump_db', method=['GET', 'POST'])
def dump_db(ctx: Context):
    flash = ctx.flash
    query = ctx.request.query
    cdb = query.get('cdb', None)
    if not cdb:
        flash.set(ctx, 'No database to dump. Please select a database to dump', 'warning')
        redirect(ctx.URL('db_admin'))
    else:
        db = ctx.ask(cdb)
        if db:
            filename = settings.DOWNLOAD_FOLDER+'/database_'+cdb+'.csv' 
            with open(filename, 'w', encoding='utf-8', newline='') as dumpfile:
                try:
                    db.export_to_csv_file(dumpfile)
                    flash.set(ctx, 'Exported db to %s' % filename, 'success')
                except Exception as e:
                    flash.set(ctx, str(e),'danger')
                redirect(ctx.URL('db_admin'))
        else:
            flash.set(ctx, 'Could not open database. Please check your db connection', 'danger')
        
    return {} 

@app.route('upload_db', method=['GET', 'POST'])
def upload_db(ctx: Context):
    flash = ctx.flash
    query = ctx.request.query
    cdb = query.get('cdb', None)
    if not cdb:
        flash.set(ctx, 'No database to upload. Please select a database to upload', 'warning')
        redirect(ctx.URL('db_admin'))
    else:
        try:
            db = ctx.ask(cdb)
            if db:
                filename = settings.UPLOAD_FOLDER+'/database_'+cdb+'.csv' 
                db.import_from_csv_file(open(filename, 'r', encoding='utf-8', newline=''))
                flash.set(ctx, 'Uploaded db from %s' % filename, 'success')
                redirect(ctx.URL('db_admin'))
            else:
                flash.set(ctx, 'Could not open database. Please check your db connection', 'danger')

        except Exception as e:
            flash.set(ctx, str(e), 'danger')

        finally:
            redirect(ctx.URL('db_admin'))
            
@app.route('table_admin', method=['GET', 'POST'])
@app.use(dat.grid_template)
def table_admin(ctx: Context):
    session = ctx.session
    flash = ctx.flash
    navbar = ctx.navbar
    menu = ctx.menu
    query = ctx.request.query
    cdb = session.get('cdb')
    table = query.get('table', None)
    db = ctx.ask(cdb)
    if not table or not cdb:
        flash.set(ctx, 'No db or table selected', 'danger')
        redirect(ctx.URL('db_admin'))
    else:
        grid=SQLGrid(ctx, 'db', db[table], upload=True, download=True, page_title='Table Admin for table %s' % table.title())
    
        if grid().accepted:
            print('Grid is good')
        else:
            print('Grid is bad')
        return dict(grid= grid.get_options())        
    
    
@app.route('actions', method=['GET', 'POST'])
@app.use(dat.action_template)
def action(ctx: Context):
    session = ctx.session
    flash=ctx.flash
    navbar = ctx.navbar
    menu = ctx.menu
    
    query = ctx.request.query
    action = query.get("action")
    
    cdb = session.get('cdb')
    db = ctx.ask(cdb)
    
    table = query.get('table')
    show_buttons=True
        
    if not action or not table:
        flash.set(ctx, 'No action or table selected', 'danger')
        redirect(ctx.URL('db_admin'))
        
    else:
        form = SQLForm(db[table]) #intialise our form
        if action == 'create':
            if form.process(ctx, db, db[table], None).accepted:
                if ctx.request.method == 'POST':
                    flash.set(ctx, 'Added okay', 'success')
                    redirect(ctx.URL('table_admin', vars=dict(cdb=cdb, table=table)))

            
        elif action == 'update':
            id = query.get('id', None)
            if not id:
                flash.set(ctx, 'You have not provided an ID', 'warning')
                redirect(ctx.URL('db_admin'))
            for fld in db[table]:
                fld.readable = fld.writable = True
            
            todo = db(db[table].id == int(id)).select().first()
            
            if form.process(ctx, db, db[table], todo).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('db_admin'))
    
        elif action == 'view':
            show_buttons = False
            id = query.get('id', None)
            if not id:
                flash.set(ctx, 'None or invalide id supplied', 'danger')
                redirect(ctx.URL('db_admin'))
            
            for fld in db[table]:
                fld.readable = fld.writable = True
            
            todo = db(db[table].id == int(id)).select().first()
            
            if form.process(ctx, db, db[table], todo).accepted:
                if ctx.request.method == 'POST':
                    redirect(ctx.URL('db_admin'))
    
        if action == 'delete':
            id = query.get('id', None)
            if not id:
                flash.set(ctx, 'None or invalide id supplied', 'danger')
                redirect(ctx.URL('db_admin'))
            rec = db[table](id)
            if rec is None:
                flash.set(ctx, 'No record found to delete', 'danger')
                redirect(ctx.URL("db_admin"))
            db(db[table].id == id).delete()
            db.commit()
            flash.set(ctx, 'Successfully deleted record', 'success')
            redirect(ctx.URL('table_admin', vars=dict(cdb=cdb, table=table)))
        
        elif action == 'download':
            
            filename = settings.DOWNLOAD_FOLDER+'/'+cdb+'_'+table+'.csv'
            try:
                with open(filename, 'w', encoding='utf-8', newline='') as dumpfile:
                    dumpfile.write(str(db(db[table]).select()))
            except Exception as e:
                flash.set(ctx, str(e), 'danger')
            finally:
                flash.set(ctx, 'Successfully downloaded %s ' % filename, 'success')
                redirect(ctx.URL('table_admin', vars=dict(cdb=cdb, table=table)))
                
        elif action == 'upload':
            
            filename = settings.UPLOAD_FOLDER+'/'+cdb+'_'+table+'.csv'
            try:
                with open(filename, 'r', encoding='utf-8', newline='') as dumpfile:
                    db[table].import_from_csv_file(dumpfile)
                db.commit()    
            except Exception as e:
                flash.set(ctx, str(e), 'danger')
            finally:
                flash.set(ctx, 'Successfully uploaded %s ' % filename, 'success')
                redirect(ctx.URL('table_admin', vars=dict(cdb=cdb, table=table)))
            
        return dict(form_options = form.get_options(), show_button=show_buttons)

