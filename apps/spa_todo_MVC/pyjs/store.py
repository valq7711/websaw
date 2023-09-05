from pyjsaw.typing.jstyping import undefined, JSON
from pyjsaw.typing.vuetyping import Vue


def _make_state():
    return {
        'st': JSON.parse(SPA_ENV.app_state)
    }


class AppStore:
    def __init__(self, make_state):
        if not make_state:
            make_state = _make_state
        self._vm = Vue({'data': make_state})
        self._state = self._vm.st
        self.update = self._update.bind(self)
        self.set_prop = self._set_prop.bind(self)
        self.set = self._set.bind(self)
        self.get = self._get.bind(self)

    @property
    def vm(self):
        return self._vm

    @property
    def state(self):
        return self._state

    @property
    def st(self):
        return self._state

    def _update(self, patch):
        self._patch_node(self.state, patch)

    def _patch_node(self, node, patch):
        for k in patch:
            v = patch[k]
            if v._is_patch_:
                self._patch_node(node[k], v.patch)
            else:
                self._set(node, k, v)

    def _set_prop(self, node, k, v):
        self._vm.S_set(node, k, v)

    def _set(self, *path_v):
        vm = self._vm
        v = path_v.pop()
        k = path_v.pop()
        path = path_v
        cur = self._vm.st
        for p in path:
            if cur[p] is undefined:
                vm.S_set(cur, p, {})
            cur = cur[p]
        vm.S_set(cur, k, v)

    def _get(self, *path):
        cur = self._vm.st
        for p in path:
            cur = cur[p]
        return cur
