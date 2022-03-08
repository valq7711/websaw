from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture

class Context(DefaultContext):
    ...


ctx_ = Context()
app = DefaultApp(ctx_, name=__package__)


# To make template replaceable/referenceable we should assign a fixture key (e.g. welcome_templ)
# To do that use the following syntax for template:
# '<fixture_key>:<template.html>'
@app.route('welcome')
@app.use('welcome_templ:welcome.html')
def welcome(ctx):
    return dict(msg='Hey! this is message from info-mixin cntroller')


@app.route('welcome_template_overwritten')
@app.use('welcome_templ_overwrite:welcome.html')
def welcome_overwite_template(ctx):
    return dict(msg='Hey! this is message from info-mixin cntroller')

@app.route('info/app')
def info_app(ctx: Context):
    def rep(v):
        if isinstance(v, list):
            return [rep(_) for _ in v]
        if isinstance(v, str):
            return v
        return repr(v)

    ret = {
        k: rep(v) for k, v in ctx.app_data.__dict__.items()
    }
    return ret
