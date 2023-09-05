from pyjsaw.typing.jstyping import Object, this, undefined, String

HTTP_METHODS = 'get post put patch delete head'.split(' ')


def _make_meth(meth_name):
    def meth(*args):
        return this._http(meth_name, *args)
    return meth


def _inject_http_methods(cls):
    meth: str
    for m in iter(HTTP_METHODS):
        cls.prototype['_' + m] = _make_meth(m)
    return cls


@_inject_http_methods
class API:
    def __init__(self, axios, baseURL, axios_opt):
        self.headers_getter = lambda : {}  # noqa
        self.baseURL = baseURL
        axios_opt = axios_opt or {}
        self.srv = axios.create(axios_opt)
        self.http = self._http.bind(self)
        for m in HTTP_METHODS:
            self[m] = self['_' + m].bind(self)

    def _http(self, meth, path_query, data_or_get_headers, headers):
        meth = meth.toLowerCase()
        query = None
        if type(path_query) is String:
            path = path_query
        else:  # array
            # the last element may be query params
            if type(path_query[-1]) is Object:
                query = path_query.pop()
            path = path_query.join('/')
        if meth in ['get', 'head']:
            data = None
            if headers is undefined:
                headers = data_or_get_headers
        else:
            data = data_or_get_headers

        if not path.startsWith('/'):
            path = f'{self.baseURL}/{path}'

        conf = {
            'method': meth,
            'url': path,
        }
        if query and len(query):
            conf.params = query
        if data:
            conf.data = data
        if headers and len(headers):
            conf.headers = Object.assign({}, headers, self.headers_getter(conf))
        else:
            conf.headers = self.headers_getter(conf)
        return self.srv.request(conf)
