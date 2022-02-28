from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture
import ombott


ombott.default_app().setup(dict(debug=True))


# make a simple custom fixture that uses another fixture (session)
class LastVisited(Fixture):
    def take_off(self, ctx: DefaultContext):
        session = ctx.session  # magic goes here - we touch session and ctx activates it!
        last_visited = session.get('last_visited', [])
        last_visited.append(ctx.request.path)
        last_visited = last_visited[-5:]
        session['last_visited'] = last_visited


# extend default context with our fixture
class Context(DefaultContext):
    track_visited = LastVisited()


ctx_ = Context()
app = DefaultApp(ctx_, dict(group_name='websaw_apps_group_one'))


@app.route('index')
@app.use(ctx_.track_visited)  # note there is no session, but it used!
def index(ctx):
    ret = {
        k: ctx[k]
        for k in 'app_name base_url static_base_url folder template_folder static_folder'.split()
    }
    ret['app_data_keys'] = [*ctx.app_data.__dict__]
    return ret


@app.route('session')
def session(ctx: DefaultContext):
    ret = {
        'group_session_data': {**ctx.group_session},
        'session_data': {**ctx.session},
        'local_data_keys': [*ctx.session.data.__dict__],
    }
    return ret

# let's go to:
# http://127.0.0.1:8000/simple
# http://127.0.0.1:8000/simple/index
# http://127.0.0.1:8000/simple/session
