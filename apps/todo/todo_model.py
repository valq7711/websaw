import datetime

from websaw import DefaultContext

from voodoodal import Table, Field

from pydal import DAL

def get_time_stripped():
    fulltime = datetime.datetime.utcnow()
    stripped = fulltime.strftime('%Y-%m-%d %H:%M:%S')
    retval = stripped.replace("T"," ")
    return retval.replace("T"," ")

class TodoModel(DAL):
    class todo(Table):
        item = Field('string', label='Todo Item')
        notes = Field('text', label = 'Notes to me')
        date_added = Field('datetime', default=get_time_stripped, readable=False, writable=False)
