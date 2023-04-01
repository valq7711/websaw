from websaw import DAL
from voodoodal import ModelBuilder
import os

from .app_model import AppModel
from ..common.common_models import AuthModel

from . import settings

_db = DAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)

# All magic goes here. We will use both the AuthModel and our local AppModel to create a comvined
# database for our app. This is purely to demonstrate the power of voodoodal and is not necessary
# if not required

@ModelBuilder(_db)
class db(AuthModel, AppModel):
    pass

assert db is _db
db.commit()

def get_download_url(picture):
    return f"images/{picture}"

db.profile.image.uploadfolder = settings.UPLOAD_PATH
db.profile.image.download_url = settings.UPLOAD_PATH
