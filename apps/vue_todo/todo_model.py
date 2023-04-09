from voodoodal import Table, Field
from pydal import DAL


class TodoModel(DAL):
    class todo(Table):
        item = Field('string', label='Todo Item')
        extra = Field('string', default='extra')
