from pyjsaw.typing.jstyping import Object, arguments, this, Promise, Error


class MergeCall:
    def set_key(self, a):
        self.cmd = 'set_key'
        self.args = a
        return self

    def merge(self, a):
        self.cmd = 'merge'
        self.args = a
        return self


class AsyncerError(Error):
    def __init__(self, msg, fun):
        super(msg)
        self.wrapped = fun


def asyncer(fun):
    merge_call = {}

    def wrap(ctx):
        def pret(ok, err):
            def inner(f, opt):
                if opt:
                    ret_v = opt.ret_v
                    ret_throw = opt.ret_throw
                    merge_key = opt.merge_key

                def _err(e, merge_key):
                    try:
                        raise e
                    except Exception as e:
                        err(e)
                    if merge_key:
                        merge_call[merge_key].map(lambda cb: cb.err(e))
                        del merge_call[merge_key]

                if ret_throw:
                    v = ret_throw
                else:
                    try:
                        if not f:
                            f = fun.apply(ctx.self, ctx.args)
                            if not (f and f.next):
                                fname = fun.__name__ or fun.name or '<anonymous>'
                                raise AsyncerError(f'{fname} must be instance of Generator', fun)
                        v = f.next(ret_v)
                    except Exception as e:
                        _err(e, merge_key)
                        return

                def resolve_cb(ret_v):
                    inner(f, {'ret_v': ret_v, 'merge_key': merge_key})

                def reject_cb(e):
                    try:
                        v = f.throw(e)
                    except Exception as e:
                        _err(e, merge_key)
                        return
                    inner(f, {'ret_throw': v, 'merge_key': merge_key})

                if isinstance(v.value, MergeCall):
                    if v.value.cmd == 'get_keys':
                        Promise.resolve(Object.keys(merge_call)).then(resolve_cb)
                    elif v.value.cmd == 'merge':
                        p = merge_call[v.value.args]
                        if p:
                            p.push({'ok': lambda v: ok(v), 'err': lambda v: err(v)})
                            return
                        else:
                            merge_key = v.value.args
                            merge_call[merge_key] = []
                            Promise.resolve(None).then(resolve_cb)
                    else:
                        Promise.resolve(None).then(resolve_cb)
                elif not v.done:
                    if isinstance(v.value, Promise):
                        v.value.then(resolve_cb,reject_cb)
                    else:
                        Promise.resolve(v.value).then(resolve_cb)
                else:
                    ok(v.value)
                    if merge_key:
                        merge_call[merge_key].map(lambda cb: cb.ok(v.value))
                        del merge_call[merge_key]
            inner()
        return pret

    def ret():
        ctx = {'self': this, 'args': arguments}
        p = Promise(wrap(ctx))
        return p
    ret.__name__ = fun.__name__ or fun.name
    return ret
