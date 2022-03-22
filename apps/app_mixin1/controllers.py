import os
from websaw import DefaultApp, DefaultContext, XAuth, AuthErr, redirect
from websaw.core import Fixture
from .models import auth_db
from .form_1 import Form, FormStyleBulma
from pydal import Field
from .common import app, ctx_, resize_image, cleanup_image
from pprint import pprint
import json

