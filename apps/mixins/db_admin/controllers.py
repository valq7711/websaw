from websaw import DefaultApp, DefaultContext, redirect
from websaw.core import Fixture
from pydal import Field
from ...auth.form_1 import Form, FormStyleBulma
import json

class Context(DefaultContext):
    ...
ctx_ = Context()
app = DefaultApp(ctx_, name=__package__)

