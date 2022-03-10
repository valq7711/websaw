from websaw import DefaultApp, DefaultContext
from websaw.core import Fixture
import ombott
from .fixtures import auth
from .models import db, auth_db, another_db
ombott.default_app().setup(dict(debug=True))

# extend default context with our fixture
class DBRegistry(Fixture):
    def __init__(self):
        self.dbs_keys = set()

class Context(DefaultContext):
    auth = auth
    auth_db = auth_db
    main_db = db
    antoher_db = another_db
    db_reg = DBRegistry()  

ctx_ = Context()
app = DefaultApp(ctx_, dict(group_name='websaw_apps_group_one'), name=__package__ )
