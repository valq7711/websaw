from websaw import DefaultContext, DefaultApp, HTTP
import json
import html


from . import utemplates as ut

class Context(DefaultContext):
    ...

ctxd = Context()

app = DefaultApp(ctxd, name=__package__)

spa = app.spa()


def json_escaped(dct):
    s = json.dumps(dct, ensure_ascii=False)
    return html.escape(s, quote=True)


@spa.main('index')  # SPA entry point
@app.use(ut.index)
def index(ctx, **kw):

    # initial app state
    app_state = dict(
        spa_todo_mvc={},
    )
    return dict(spa_name=spa.name, app_state=json_escaped(app_state))


# spa-part of index-page
@spa.route('index')
@app.use('#todo')   # use page `pyjsaw/pages/todo.py>`
def spa_todo(ctx, **kw):
    return dict(msg='Hey there!')
