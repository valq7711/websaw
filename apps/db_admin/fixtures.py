from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import Fixture

class Auth(XAuth):
        
    def user_by_login(self, login: str) -> dict:
        login = login.lower()
        db = self.data.ctx.auth_db
        user = db(db.auth_user.username == login).select().first()
        return user
        
    def user_for_session(self, user):
        suser = super().user_for_session(user)
        suser['email'] = user['email']
        suser['name'] = user['name']
        return suser

auth = Auth()

