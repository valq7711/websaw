from websaw import DefaultApp, DefaultContext
from websaw.fixtures import Env


class Context(DefaultContext):
    env = {'mixin_env': 'mixin env is not mixed-in since it is not secure'}
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
    ret['env'] = ctx.env
    return ret
