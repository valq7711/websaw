from websaw import DefaultContext
from websaw.fixtures import XAuth

class GetNavbar(XAuth):
    def take_on(self, ctx:DefaultContext):
        self.data.db = ctx.db
        self.data.user = ctx.user
        ## for now there is just one role per user and not app specific NEED TO CHANGE !!!!
        db = self.data.db
        role = ''
        if self.data.user:
            user_id = self.data.user['id']
        else:
            user_id = 0  # we are probabyl not logged in yet   
        member = db(db.membership.user_id == user_id).select().first()
        if not member:
            role = 'user'
        else:
            role = db.roles(member.role_id).role
        
        if not role in ctx.env['menus']:
            ctx.env['menu'] = []
        else:
            ctx.env['menu'] = ctx.env['menus'][role]
