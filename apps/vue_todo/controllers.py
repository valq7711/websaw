from websaw import DefaultContext, DefaultApp, HTTP, redirect, URL

from . import utemplates as ut
from .todo_db import db


class Context(DefaultContext):
    db = db


ctxd = Context()

app = DefaultApp(ctxd, name=__package__)


@app.route('index', ['GET', 'POST'])
@app.use(ut.index)
def index(ctx: Context, **kw):
    db = ctx.db
    items = db(db.todo).select()
    return {'todos_options': dict(todo_items=items.as_dict(), api_controller='todo')}


@app.route('todo', method=['GET', 'POST'])
@app.route('todo/:id', method=['POST', 'DELETE'])
def todo(ctx: Context, id=None):
    db = ctx.db
    if id:
        id = int(id)
    meth = ctx.request.method
    if meth == 'POST':
        item = ctx.request.json.get('item')
        if id:
            db(db.todo.id == id).update(item=item)
        else:
            db.todo.insert(item=item)

    elif meth == 'DELETE':
        db(db.todo.id == id).delete()

    items = db(db.todo).select()
    return {'items': items.as_dict()}
