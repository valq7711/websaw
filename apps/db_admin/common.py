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
app = DefaultApp(ctx_, dict(group_name='websaw_apps_group_one'))



#not tested but should work
#ctx.db_reg.dbs_keys - all db-keys of the current app
#I mean DAL-fixture  - should be fixed, or you can just 
#class myDAL(DAL):
#    def app_mounted(self, ctx):
#        # see above
#and use myDAL  instead of DAL everywhere
#as variant you can self.dbs_meta = {}
#and db_reg.dbs_meta[self_key] = some_meta_about_this_db

'''



class Context(DefaultContext):
    auth = auth
    default_db = db
    
ctx_ = Context()
app = DefaultApp(ctx_, dict(group_name='websaw_apps_group_one'))
'''
