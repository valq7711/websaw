from websaw import DAL
from voodoodal import ModelBuilder
import os

from .blog_model import BlogModel
from ..common.common_models import AuthModel

from . import settings

_db = DAL(
    "sqlite://storage.db", folder=os.path.join(os.path.dirname(__file__), "databases")
)

# All magic goes here
@ModelBuilder(_db)
class db(AuthModel, BlogModel):
    pass

assert db is _db
db.commit()

def get_download_url(picture):
    return f"images/{picture}"

db.profile.image.uploadfolder = settings.UPLOAD_PATH
db.profile.image.download_url = settings.UPLOAD_PATH
