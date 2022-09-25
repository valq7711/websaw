from websaw import DAL
from voodoodal import ModelBuilder
from . import settings
import os

from ... common.common_models import AuthModel


_db = DAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)

# All magic goes here
@ModelBuilder(_db)
class db(AuthModel):
    pass


assert db is _db
db.commit()

db.profile.image.uploadfolder = settings.UPLOAD_PATH
db.profile.image.download_url = settings.UPLOAD_PATH
