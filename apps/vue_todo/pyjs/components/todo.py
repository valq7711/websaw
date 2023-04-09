from pyjsaw.typing.jstyping import window, String, Object
from pyjsaw.js_stuff.vuestuff import VTempl, VDot as v
from pyjsaw.js_stuff import html as h
from pyjsaw.pyjs.vcollector import vc

from asset.server import API
from asset.asyncer import asyncer


ENV = window.WEBSAW_ENV

srv_api = API(axios, ENV.app_base)


templ = VTempl({
    h.Div(): {
        h.H1(): 'TODO',
        h.Div(v.For('it in items'), v.bind(key='it.id')): {
            h.Span(): 'id:{{it.id}}',
            h.Input(v.model('it.item'), v.on(change='update(it.id)')): None,
            h.Button(v.on(click='remove(it.id)')): 'Remove'
        },
        h.Div(): {
            h.Input(v.model('new_item'), v.on(changed='insert')): None,
            h.Button(v.on(click='insert')): 'Add',
        }
    }
})


@vc.component()
class Todo:

    template = templ

    api = String, ''
    todos = Object, None

    def data(data_obj, vm: 'Todo'):
        data_obj.new_item = None
        data_obj.items = {**vm.todos}

    @asyncer
    def reload(self):
        resp = yield srv_api.get(self.api)
        self.items = resp.data.items

    @asyncer
    def insert(self):
        resp = yield srv_api.post(self.api, {'item': self.new_item})
        self.items = resp.data.items

    @asyncer
    def update(self, id):
        resp = yield srv_api.post([self.api, id], {'item': self.items[id].item})
        self.items = resp.data.items

    @asyncer
    def remove(self, id):
        resp = yield srv_api.delete([self.api, id])
        self.items = resp.data.items


def make():
    return Todo
