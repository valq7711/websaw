(function(){
"use strict";
var ՐՏ_2, ՐՏ_3;
function ՐՏ_extends(child, parent) {
    child.prototype = Object.create(parent.prototype);
    child.prototype.__base__ = parent;
    child.prototype.constructor = child;
}
function ՐՏ_in(val, arr) {
    if (typeof arr.indexOf === "function") {
        return arr.indexOf(val) !== -1;
    } else if (typeof arr.has === "function") {
        return arr.has(val);
    }
    return arr.hasOwnProperty(val);
}
function ՐՏ_Iterable(iterable) {
    var tmp;
    if (iterable.constructor === [].constructor || iterable.constructor === "".constructor || (tmp = Array.prototype.slice.call(iterable)).length) {
        return tmp || iterable;
    }
    if (Set && iterable.constructor === Set) {
        return Array.from(iterable);
    }
    return Object.keys(iterable);
}
function len(obj) {
    var tmp;
    if (obj.constructor === [].constructor || obj.constructor === "".constructor || (tmp = Array.prototype.slice.call(obj)).length) {
        return (tmp || obj).length;
    }
    if (Set && obj.constructor === Set) {
        return obj.size;
    }
    return Object.keys(obj).length;
}
function range(start, stop, step) {
    var length, idx, range;
    if (arguments.length <= 1) {
        stop = start || 0;
        start = 0;
    }
    step = arguments[2] || 1;
    length = Math.max(Math.ceil((stop - start) / step), 0);
    idx = 0;
    range = new Array(length);
    while (idx < length) {
        range[idx++] = start;
        start += step;
    }
    return range;
}
function ՐՏ_type(obj) {
    return obj && obj.constructor && obj.constructor.name ? obj.constructor.name : Object.prototype.toString.call(obj).slice(8, -1);
}
function ՐՏ_eq(a, b) {
    var ՐՏitr11, ՐՏidx11;
    var i;
    if (a === b) {
        return true;
    }
    if (a === void 0 || b === void 0 || a === null || b === null) {
        return false;
    }
    if (a.constructor !== b.constructor) {
        return false;
    }
    if (Array.isArray(a)) {
        if (a.length !== b.length) {
            return false;
        }
        for (i = 0; i < a.length; i++) {
            if (!ՐՏ_eq(a[i], b[i])) {
                return false;
            }
        }
        return true;
    } else if (a.constructor === Object) {
        if (Object.keys(a).length !== Object.keys(b).length) {
            return false;
        }
        ՐՏitr11 = ՐՏ_Iterable(a);
        for (ՐՏidx11 = 0; ՐՏidx11 < ՐՏitr11.length; ՐՏidx11++) {
            i = ՐՏitr11[ՐՏidx11];
            if (!ՐՏ_eq(a[i], b[i])) {
                return false;
            }
        }
        return true;
    } else if (Set && a.constructor === Set || Map && a.constructor === Map) {
        if (a.size !== b.size) {
            return false;
        }
        for (i of a) {
            if (!b.has(i)) {
                return false;
            }
        }
        return true;
    } else if (a.constructor === Date) {
        return a.getTime() === b.getTime();
    } else if (typeof a.__eq__ === "function") {
        return a.__eq__(b);
    }
    return false;
}
function ՐՏ_def_modules() {
    var modules;
    modules = {};
    function mounter(mod_id) {
        var rs_mod_id, rs_mod;
        rs_mod_id = "ՐՏ:" + mod_id;
        rs_mod = modules[rs_mod_id] = {
            "body": null,
            "exports": null
        };
        rs_mod["export"] = function(prop, get, set) {
            if (!rs_mod["exports"]) {
                rs_mod["exports"] = {};
            }
            Object.defineProperty(rs_mod["exports"], prop, {
                configurable: true,
                enumerable: true,
                get: get,
                set: set
            });
        };
        Object.defineProperty(modules, mod_id, {
            enumerable: true,
            get: function() {
                var mod;
                return (mod = modules[rs_mod_id])["exports"] || mod["body"]();
            },
            set: function(v) {
                modules[rs_mod_id]["exports"] = v;
            }
        });
        return rs_mod;
    }
    Object.defineProperty(modules, "ՐՏ_def", {
        configurable: false,
        enumerable: false,
        value: mounter
    });
    return modules;
}
var ՐՏ_modules = ՐՏ_def_modules();
ՐՏ_modules.ՐՏ_def("asset.rs_vue");
ՐՏ_modules.ՐՏ_def("asset.asyncer");
ՐՏ_modules.ՐՏ_def("asset.server");
ՐՏ_modules.ՐՏ_def("asset");

ՐՏ_modules["ՐՏ:asset.rs_vue"].body = function(){
    var __name__ = "asset.rs_vue";

    function is_hook(name) {
        return [ "beforeCreate", "created", "beforeMount", "mounted", "beforeUpdate", "updated", "activated", "deactivated", "beforeDestroy", "destroyed", "render" ].includes(name);
    }
    function is_special(name) {
        return /^(_.+|constructor)$/.test(name);
    }
    class RS_vue {
        constructor (v_collector, name) {
            var ՐՏ_1, ՐՏitr1, ՐՏidx1, ՐՏitr2, ՐՏidx2, ՐՏitr3, ՐՏidx3;
            var self = this;
            var tmp, bases, it, sym, _name, k, methods, meth;
            if (!v_collector) {
                v_collector = self.__vue_opt__;
            } else if (ՐՏ_type(v_collector) === "String") {
                name = v_collector;
                v_collector = self.__vue_opt__;
            }
            if (name) {
                self.name = (ՐՏ_1 = name.split("."))[ՐՏ_1.length-1];
            }
            self.props = {};
            if (tmp = self.data || self._init_data) {
                self.data = tmp;
            }
            self.methods = {};
            if (v_collector) {
                if ((bases = v_collector.bases) && bases.length) {
                    self.mixins = v_collector.bases;
                }
                self.computed = v_collector._computed;
                self.directives = v_collector._directives;
                self.filters = v_collector._filters;
                self.watch = v_collector._watch;
                Object.assign(self.methods, v_collector._methods);
                ՐՏitr1 = ՐՏ_Iterable([ [ "~", "_mutations" ], [ "*", "_actions" ] ]);
                for (ՐՏidx1 = 0; ՐՏidx1 < ՐՏitr1.length; ՐՏidx1++) {
                    it = ՐՏitr1[ՐՏidx1];
                    [sym, _name] = it;
                    if (v_collector[_name]) {
                        if (!self.map_store) {
                            self.map_store = {};
                        }
                        ՐՏitr2 = ՐՏ_Iterable(v_collector[_name]);
                        for (ՐՏidx2 = 0; ՐՏidx2 < ՐՏitr2.length; ՐՏidx2++) {
                            k = ՐՏitr2[ՐՏidx2];
                            self.map_store[k] = sym;
                            self.methods[k] = v_collector[_name][k];
                        }
                    }
                }
            }
            methods = Object.getOwnPropertyDescriptors(self.__proto__);
            ՐՏitr3 = ՐՏ_Iterable(methods);
            for (ՐՏidx3 = 0; ՐՏidx3 < ՐՏitr3.length; ՐՏidx3++) {
                meth = ՐՏitr3[ՐՏidx3];
                if (is_special(meth) || v_collector && v_collector.__collected__[meth]) {
                    continue;
                }
                if (is_hook(meth)) {
                    self[meth] = methods[meth].value;
                } else if (methods[meth].value.call) {
                    self.methods[meth] = methods[meth].value;
                }
            }
        }
        static make () {
            var args = [].slice.call(arguments, 0);
            var cls;
            cls = this;
            return new cls(...args);
        }
    }
    function unpack_name_fun_opt(f_reg_as) {
        function unpacker(reg_as, name_fun_opt, opt) {
            var self, arg1type, name;
            self = this;
            if (!name_fun_opt) {
                if (reg_as === "_getters") {
                    return function(f) {
                        var name;
                        name = f.__name__ || f.name;
                        return f_reg_as.call(self, reg_as, name, f());
                    };
                } else {
                    throw new Error("Attempt to call V_Collector @decorator with empty `()`");
                }
            }
            arg1type = ՐՏ_type(name_fun_opt);
            if (arg1type.startsWith("Fun")) {
                name = name_fun_opt.__name__ || name_fun_opt.name;
                return f_reg_as.call(self, reg_as, name, name_fun_opt);
            } else {
                return function(f) {
                    var name;
                    if (arg1type.startsWith("Str")) {
                        name = name_fun_opt;
                        if (opt) {
                            opt.handler = f;
                        } else {
                            opt = f;
                        }
                    } else {
                        opt = name_fun_opt;
                        name = f.__name__ || f.name;
                        opt.handler = f;
                    }
                    return f_reg_as.call(self, reg_as, name, opt);
                };
            }
        }
        return unpacker;
    }
    var V_collector = (ՐՏ_2 = class V_collector {
        constructor () {
            var self = this;
            self._methods = null;
            self._computed = null;
            self._watch = null;
            self._filters = null;
            self._directives = null;
            self._getters = null;
            self._mutations = null;
            self._actions = null;
            self.__current__ = null;
            self.__collected__ = {};
        }
        _collector (opt_name, extra) {
            var self = this;
            self.__current__ = {
                __collected__: {}
            };
            if (extra) {
                Object.assign(self.__current__, extra);
            }
            function wrapper(cls) {
                cls.prototype[opt_name] = self.__current__;
                cls.prototype.name = cls.name;
                self.__current__ = null;
                return cls;
            }
            return wrapper;
        }
        component () {
            var self = this;
            var bases = [].slice.call(arguments, 0);
            return self._collector("__vue_opt__", {
                bases: bases
            });
        }
        store () {
            var self = this;
            return self._collector("__store_opt__");
        }
        _reg_as (reg_as, name, fun_opt) {
            var self = this;
            var cur;
            cur = self.__current__ || self;
            if (!cur[reg_as]) {
                cur[reg_as] = {};
            }
            cur[reg_as][name] = fun_opt;
            cur.__collected__[name] = true;
            return fun_opt.handler ? fun_opt.handler : fun_opt;
        }
        meth (name_or_fun) {
            var self = this;
            return self._reg_as("_methods", name_or_fun);
        }
        computed (name_or_fun) {
            var self = this;
            return self._reg_as("_computed", name_or_fun);
        }
        filter (name_or_fun) {
            var self = this;
            return self._reg_as("_filters", name_or_fun);
        }
        directive (name_or_fun) {
            var self = this;
            return self._reg_as("_directives", name_or_fun);
        }
        watch (name_or_fun, opt) {
            var self = this;
            return self._reg_as("_watch", name_or_fun, opt);
        }
        getter (name_or_fun) {
            var self = this;
            return self._reg_as("_getters", name_or_fun);
        }
        model (name_or_fun) {
            var self = this;
            return self._reg_as("_getters")(name_or_fun);
        }
        mutation (name_or_fun) {
            var self = this;
            return self._reg_as("_mutations", name_or_fun);
        }
        action (name_or_fun) {
            var self = this;
            return self._reg_as("_actions", name_or_fun);
        }
    }, (function(){
        Object.defineProperties(ՐՏ_2.prototype, {
            _reg_as: {
                enumerable: false, 
                writable: true, 
                value: unpack_name_fun_opt(ՐՏ_2.prototype._reg_as)
            }
        });
        return ՐՏ_2;
    })(), ՐՏ_2);
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.rs_vue"];
    ՐՏ_mod.export("is_hook", function(){return is_hook;}, function(ՐՏ_v){if (typeof is_hook !== "undefined") {is_hook = ՐՏ_v;};});
    ՐՏ_mod.export("is_special", function(){return is_special;}, function(ՐՏ_v){if (typeof is_special !== "undefined") {is_special = ՐՏ_v;};});
    ՐՏ_mod.export("RS_vue", function(){return RS_vue;}, function(ՐՏ_v){if (typeof RS_vue !== "undefined") {RS_vue = ՐՏ_v;};});
    ՐՏ_mod.export("unpack_name_fun_opt", function(){return unpack_name_fun_opt;}, function(ՐՏ_v){if (typeof unpack_name_fun_opt !== "undefined") {unpack_name_fun_opt = ՐՏ_v;};});
    ՐՏ_mod.export("V_collector", function(){return V_collector;}, function(ՐՏ_v){if (typeof V_collector !== "undefined") {V_collector = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset.asyncer"].body = function(){
    var __name__ = "asset.asyncer";

    class MergeCall {
        set_key (a) {
            var self = this;
            self.cmd = "set_key";
            self.args = a;
            return self;
        }
        merge (a) {
            var self = this;
            self.cmd = "merge";
            self.args = a;
            return self;
        }
    }
    class AsyncerError extends Error {
        constructor (msg, fun) {
            super(msg);
            var self = this;
            self.wrapped = fun;
        }
    }
    function asyncer(fun) {
        var merge_call, ret;
        merge_call = {};
        function wrap(ctx) {
            function pret(ok, err) {
                function inner(f, opt) {
                    var ret_v, ret_throw, merge_key, v, fname, p;
                    if (opt) {
                        ret_v = opt.ret_v;
                        ret_throw = opt.ret_throw;
                        merge_key = opt.merge_key;
                    }
                    function _err(e, merge_key) {
                        try {
                            throw e;
                        } catch (ՐՏ_Exception) {
                            err(e);
                        }
                        if (merge_key) {
                            merge_call[merge_key].map(function(cb) {
                                cb.err(e);
                            });
                            delete merge_call[merge_key];
                        }
                    }
                    if (ret_throw) {
                        v = ret_throw;
                    } else {
                        try {
                            if (!f) {
                                f = fun.apply(ctx.self, ctx.args);
                                if (!(f && f.next)) {
                                    fname = fun.__name__ || fun.name || "<anonymous>";
                                    throw new AsyncerError(`${fname} must be instance of Generator`, fun);
                                }
                            }
                            v = f.next(ret_v);
                        } catch (ՐՏ_Exception) {
                            var e = ՐՏ_Exception;
                            _err(e, merge_key);
                            return;
                        }
                    }
                    if (v.value instanceof MergeCall) {
                        if (v.value.cmd === "get_keys") {
                            Promise.resolve(Object.keys(merge_call)).then(function(ret_v) {
                                inner(f, {
                                    ret_v: ret_v,
                                    merge_key: merge_key
                                });
                            });
                        } else if (v.value.cmd === "merge") {
                            if (p = merge_call[v.value.args]) {
                                p.push({
                                    ok: function(v) {
                                        ok(v);
                                    },
                                    err: function(v) {
                                        err(v);
                                    }
                                });
                                return;
                            } else {
                                merge_key = v.value.args;
                                merge_call[merge_key] = [];
                                Promise.resolve(null).then(function(ret_v) {
                                    inner(f, {
                                        ret_v: ret_v,
                                        merge_key: merge_key
                                    });
                                });
                            }
                        } else {
                            Promise.resolve(null).then(function(ret_v) {
                                inner(f, {
                                    ret_v: ret_v,
                                    merge_key: merge_key
                                });
                            });
                        }
                    } else if (!v.done) {
                        if (v.value instanceof Promise) {
                            v.value.then(function(ret_v) {
                                inner(f, {
                                    ret_v: ret_v,
                                    merge_key: merge_key
                                });
                            }, function(e) {
                                var v;
                                try {
                                    v = f.throw(e);
                                } catch (ՐՏ_Exception) {
                                    var e = ՐՏ_Exception;
                                    _err(e, merge_key);
                                    return;
                                }
                                inner(f, {
                                    ret_throw: v,
                                    merge_key: merge_key
                                });
                            });
                        } else {
                            Promise.resolve(v.value).then(function(ret_v) {
                                inner(f, {
                                    ret_v: ret_v,
                                    merge_key: merge_key
                                });
                            });
                        }
                    } else {
                        ok(v.value);
                        if (merge_key) {
                            merge_call[merge_key].map(function(cb) {
                                cb.ok(v.value);
                            });
                            delete merge_call[merge_key];
                        }
                    }
                }
                inner();
            }
            return pret;
        }
        ret = function() {
            var ctx, p;
            ctx = {
                self: this,
                args: arguments
            };
            p = new Promise(wrap(ctx));
            return p;
        };
        ret.__name__ = fun.__name__ || fun.name;
        return ret;
    }
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.asyncer"];
    ՐՏ_mod.export("MergeCall", function(){return MergeCall;}, function(ՐՏ_v){if (typeof MergeCall !== "undefined") {MergeCall = ՐՏ_v;};});
    ՐՏ_mod.export("AsyncerError", function(){return AsyncerError;}, function(ՐՏ_v){if (typeof AsyncerError !== "undefined") {AsyncerError = ՐՏ_v;};});
    ՐՏ_mod.export("asyncer", function(){return asyncer;}, function(ՐՏ_v){if (typeof asyncer !== "undefined") {asyncer = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset.server"].body = function(){
    var __name__ = "asset.server";

    var HTTP_METHODS;
    HTTP_METHODS = "get post put patch delete head".split(" ");
    function inject_http_methods(cls) {
        var ՐՏitr4, ՐՏidx4;
        var m;
        ՐՏitr4 = ՐՏ_Iterable(HTTP_METHODS);
        for (ՐՏidx4 = 0; ՐՏidx4 < ՐՏitr4.length; ՐՏidx4++) {
            m = ՐՏitr4[ՐՏidx4];
            const meth = m;
            cls.prototype["_" + meth] = function() {
                var args = [].slice.call(arguments, 0);
                return this._http(meth, ...args);
            };
        }
        return cls;
    }
    
    var API = (ՐՏ_3 = class API {
        constructor (axios, baseURL, axios_opt) {
            var ՐՏitr5, ՐՏidx5;
            var self = this;
            var m;
            self.baseURL = baseURL;
            axios_opt = axios_opt || {};
            self.srv = axios.create(axios_opt);
            self.http = self._http.bind(self);
            ՐՏitr5 = ՐՏ_Iterable(HTTP_METHODS);
            for (ՐՏidx5 = 0; ՐՏidx5 < ՐՏitr5.length; ՐՏidx5++) {
                m = ՐՏitr5[ՐՏidx5];
                self[m] = self["_" + m].bind(self);
            }
        }
        _http (meth, path_query, data_or_get_headers, headers) {
            var self = this;
            var query, path, data, conf;
            meth = meth.toLowerCase();
            query = null;
            if (ՐՏ_type(path_query) === "String") {
                path = path_query;
            } else {
                if (ՐՏ_type(path_query[path_query.length-1]) !== "String") {
                    query = path_query.pop();
                }
                path = path_query.join("/");
            }
            if (ՐՏ_in(meth, [ "get", "head" ])) {
                data = null;
                if (headers === void 0) {
                    headers = data_or_get_headers;
                }
            } else {
                data = data_or_get_headers;
            }
            if (!path.startsWith("/")) {
                path = `${self.baseURL}/${path}`;
            }
            conf = {
                method: meth,
                url: path
            };
            if (query && len(query)) {
                conf.params = query;
            }
            if (data) {
                conf.data = data;
            }
            if (headers && len(headers)) {
                conf.headers = headers;
            }
            return self.srv.request(conf);
        }
    }, ՐՏ_3 = inject_http_methods(ՐՏ_3), ՐՏ_3);
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.server"];
    ՐՏ_mod.export("HTTP_METHODS", function(){return HTTP_METHODS;}, function(ՐՏ_v){if (typeof HTTP_METHODS !== "undefined") {HTTP_METHODS = ՐՏ_v;};});
    ՐՏ_mod.export("inject_http_methods", function(){return inject_http_methods;}, function(ՐՏ_v){if (typeof inject_http_methods !== "undefined") {inject_http_methods = ՐՏ_v;};});
    ՐՏ_mod.export("API", function(){return API;}, function(ՐՏ_v){if (typeof API !== "undefined") {API = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset"].body = function(){
    var __name__ = "asset";

    ՐՏ_modules["ՐՏ:asset"].export("rs_vue", function(){return ՐՏ_modules["asset.rs_vue"];}, function(){throw new Error("use Object.defineProperty!");});
    ՐՏ_modules["ՐՏ:asset"].export("asyncer", function(){return ՐՏ_modules["asset.asyncer"];}, function(){throw new Error("use Object.defineProperty!");});
    ՐՏ_modules["ՐՏ:asset"].export("server", function(){return ՐՏ_modules["asset.server"];}, function(){throw new Error("use Object.defineProperty!");});

    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset"];
    return ՐՏ_mod["exports"];
};

(function(){

    var __name__ = "__main__";

    var ՐՏ_4, ՐՏ_5, ՐՏ_8, ՐՏ_10, ՐՏ_11;
    var env, amd, axios, VueRouter, api, vc, page_mixin;
    var RS_vue = ՐՏ_modules["asset.rs_vue"].RS_vue;var V_collector = ՐՏ_modules["asset.rs_vue"].V_collector;
    var asyncer = ՐՏ_modules["asset.asyncer"].asyncer;
    var API = ՐՏ_modules["asset.server"].API;
    env = window.SPA_ENV;
    amd = null;
    axios = null;
    VueRouter = null;
    api = null;
    
    var load_component = (ՐՏ_4 = function* load_component(name) {
        var c, templ;
        c = yield amd.import(`${env.spa.components}/${name}`);
        if (!(c.template || c.render)) {
            templ = name + ".html";
            c.template = (yield api.get([ env.spa.components, templ_url ])).data;
        }
        return c;
    }, ՐՏ_4 = asyncer(ՐՏ_4), ՐՏ_4);
    vc = new V_collector();
    var PageUtil = (ՐՏ_5 = class PageUtil {
        constructor (vm) {
            var self = this;
            self.vm = vm;
        }
        *http (meth, path_query, data_or_get_headers, headers) {
            var self = this;
            var resp;
            if (!path_query || !len(path_query)) {
                path_query = [ self.vm.page_api ];
            }
            if (!(path_query instanceof Array)) {
                path_query = [ path_query ];
            }
            if (len(path_query) === 1 && ՐՏ_type(path_query[0]) !== "String") {
                path_query = [ null, path_query[0] ];
            }
            if (!path_query[0]) {
                path_query[0] = self.vm.page_api;
            } else if (path_query[0].startsWith("./")) {
                path_query[0] = self.vm.page_api_root + path_query[0].slice(1);
            }
            resp = yield api.http(meth, path_query, data_or_get_headers, headers);
            self.vm.on_response(resp);
        }
        get () {
            var self = this;
            var args = [].slice.call(arguments, 0);
            var len_args, path, query, headers;
            len_args = len(args);
            [path, query, headers] = [ null, null, null ];
            if (len_args === 1) {
                path = args.pop();
            } else if (len_args === 2) {
                [path, query] = args;
            } else if (len_args === 3) {
                [path, query, headers] = args;
            }
            self.http("get", [ path, query ], headers);
        }
        post () {
            var self = this;
            var args = [].slice.call(arguments, 0);
            self.http("post", ...args);
        }
        *redirect (path, query) {
            var self = this;
            if (query === void 0 && !(ՐՏ_in(ՐՏ_type(path), [ "String", "Array" ]))) {
                query = path;
                path = null;
            }
            if (!path || path === ".") {
                path = self.vm.$route.path;
            }
            if (path[0] !== "/") {
                path = "/" + path;
            }
            if (!query) {
                query = {};
            }
            try {
                yield self.vm.$router.push({
                    path: path,
                    query: query
                });
            } catch (ՐՏ_Exception) {
                var ՐՏ_6, ՐՏ_7;
                var err = ՐՏ_Exception;
                if (err._isRouter && ((ՐՏ_6 = err.type) !== (ՐՏ_7 = VueRouter.NavigationFailureType.duplicated) && (typeof ՐՏ_6 !== "object" || !ՐՏ_eq(ՐՏ_6, ՐՏ_7)))) {
                    throw ՐՏ_Exception;
                }
                self.reload_data();
            }
        }
        reload_data () {
            var self = this;
            var r;
            r = self.vm.$route;
            self.get("." + r.path, r.query);
        }
        parse_response (r) {
            var self = this;
            var data, commands;
            data = r.data;
            commands = null;
            if (r.headers["x-sparesponse"]) {
                commands = data;
                data = commands.data || null;
                delete commands.data;
            }
            return [data, commands];
        }
    }, (function(){
        Object.defineProperties(ՐՏ_5.prototype, {
            http: {
                enumerable: false, 
                writable: true, 
                value: asyncer(ՐՏ_5.prototype.http)
            },
            redirect: {
                enumerable: false, 
                writable: true, 
                value: asyncer(ՐՏ_5.prototype.redirect)
            }
        });
        return ՐՏ_5;
    })(), ՐՏ_5);
    
    var PageMixin = (ՐՏ_8 = class PageMixin extends RS_vue {
        beforeCreate () {
            var self = this;
            self.$pu = new PageUtil(self);
            self.$data_commands = self.$pu.parse_response(self.$attrs.in_response);
        }
        on_response (r) {
            var ՐՏitr6, ՐՏidx6, ՐՏitr7, ՐՏidx7;
            var self = this;
            var data, commands, k, c, args;
            [data, commands] = self.$pu.parse_response(r);
            ՐՏitr6 = ՐՏ_Iterable(data);
            for (ՐՏidx6 = 0; ՐՏidx6 < ՐՏitr6.length; ՐՏidx6++) {
                k = ՐՏitr6[ՐՏidx6];
                self[k] = data[k];
            }
            ՐՏitr7 = ՐՏ_Iterable(commands || []);
            for (ՐՏidx7 = 0; ՐՏidx7 < ՐՏitr7.length; ՐՏidx7++) {
                c = ՐՏitr7[ՐՏidx7];
                args = commands[c];
                if (!Array.isArray(args)) {
                    args = [ args ];
                }
                self[c].call(self, ...args);
            }
        }
        redirect () {
            var self = this;
            var args = [].slice.call(arguments, 0);
            self.$pu.redirect(...args);
        }
        alert (msg) {
            var ՐՏ_9;
            var self = this;
            
            (ՐՏ_9 = function() {
                setTimeout(function() {
                    alert(msg);
                }, 100);
            }, ՐՏ_9 = self.$nextTick(ՐՏ_9), ՐՏ_9)
        }
        on_route_changed (to_, from_) {
            var self = this;
            self.$pu.get("." + to_.path, to_.query);
        }
        page_api () {
            var self = this;
            return `${self.page_api_root}${self.$route.path}`;
        }
        page_api_root () {
            var self = this;
            return `pages-api/${env.spa_name}`;
        }
    }, ՐՏ_8 = vc.component()((function(){
        Object.defineProperties(ՐՏ_8.prototype, {
            on_route_changed: {
                enumerable: false, 
                writable: true, 
                value: vc.watch("$route")(ՐՏ_8.prototype.on_route_changed)
            },
            page_api: {
                enumerable: false, 
                writable: true, 
                value: vc.computed(ՐՏ_8.prototype.page_api)
            },
            page_api_root: {
                enumerable: false, 
                writable: true, 
                value: vc.computed(ՐՏ_8.prototype.page_api_root)
            }
        });
        return ՐՏ_8;
    })()), ՐՏ_8);
    page_mixin = new PageMixin();
    
    var PageBase = (ՐՏ_10 = class PageBase extends RS_vue {
        constructor (templ) {
            super();
            var self = this;
            self.template = templ;
        }
        data () {
            var self = this;
            var ret, data, commands;
            ret = {};
            [data, commands] = self.$data_commands;
            return data;
        }
        mounted () {
            var ՐՏitr8, ՐՏidx8;
            var self = this;
            var data, commands, c, args;
            [data, commands] = self.$data_commands;
            if (!commands) {
                return;
            }
            ՐՏitr8 = ՐՏ_Iterable(commands);
            for (ՐՏidx8 = 0; ՐՏidx8 < ՐՏitr8.length; ՐՏidx8++) {
                c = ՐՏitr8[ՐՏidx8];
                args = commands[c];
                if (!Array.isArray(args)) {
                    args = [ args ];
                }
                self[c].call(self, ...args);
            }
        }
    }, ՐՏ_10 = vc.component(page_mixin)(ՐՏ_10), ՐՏ_10);
    
    var PageWrapper = (ՐՏ_11 = class PageWrapper extends RS_vue {
        constructor (component_or_url, pages) {
            super();
            var self = this;
            var pg_module, component, templ_url;
            pg_module = pages[component_or_url];
            if (pg_module) {
                component = pg_module.make();
                component.mixins = [ page_mixin ];
                templ_url = null;
            } else {
                component = null;
                templ_url = component_or_url;
            }
            self.meta = {
                templ_url: templ_url,
                component: component
            };
        }
        data () {
            var self = this;
            var meta, component_loaded;
            meta = self.meta;
            component_loaded = meta.component !== null;
            return {
                component_loaded: component_loaded,
                in_response_loaded: false
            };
        }
        beforeCreate () {
            var self = this;
            self.meta = self.$options.meta;
            self.in_response = null;
        }
        page_api_uri () {
            var self = this;
            return `pages-api/${env.spa_name}` + self.$route.fullPath;
        }
        *load_page_component () {
            var self = this;
            var meta, template, page_api_uri, module_name, module_path, component, templ_url;
            meta = self.meta;
            template = null;
            page_api_uri = self.page_api_uri();
            if (!meta.component) {
                if (meta.templ_url.endsWith(".js")) {
                    module_name = meta.templ_url.slice(0, -3);
                    module_path = [ env.app_base, "static", module_name ].join("/");
                    component = (yield amd.import(module_path));
                    if (!(component.template || component.render)) {
                        templ_url = module_name + ".html";
                        component.template = (yield api.get([ "static", templ_url ])).data;
                    }
                    component.mixins = [ page_mixin ];
                    meta.component = component;
                } else {
                    template = (yield api.get([ "static", meta.templ_url ])).data;
                    meta.component = new PageBase(template);
                }
            }
            self.component_loaded = true;
        }
        *load_data () {
            var self = this;
            var page_api_uri, response;
            page_api_uri = self.page_api_uri();
            response = (yield api.get([ page_api_uri ]));
            self.in_response = response;
            self.in_response_loaded = true;
        }
        render (h) {
            var self = this;
            var meta, component, in_response;
            meta = self.meta;
            if (!self.component_loaded) {
                self.load_page_component();
                return h({
                    template: "<div>Loading...</div>"
                });
            }
            if (!self.in_response_loaded) {
                self.load_data();
                return h({
                    template: "<div>Loading...</div>"
                });
            }
            component = meta.component;
            in_response = self.in_response;
            return h(component, {
                attrs: {
                    in_response: in_response
                }
            });
        }
    }, ՐՏ_11 = vc.component()((function(){
        Object.defineProperties(ՐՏ_11.prototype, {
            load_page_component: {
                enumerable: false, 
                writable: true, 
                value: asyncer(ՐՏ_11.prototype.load_page_component)
            },
            load_data: {
                enumerable: false, 
                writable: true, 
                value: asyncer(ՐՏ_11.prototype.load_data)
            }
        });
        return ՐՏ_11;
    })()), ՐՏ_11);
    function make_routes(routes_map, pages) {
        var ՐՏitr9, ՐՏidx9, ՐՏitr10, ՐՏidx10;
        var ret, templ_url, spa_route, route, type_prefix, component_or_url, rec;
        ret = [];
        ՐՏitr9 = ՐՏ_Iterable(routes_map);
        for (ՐՏidx9 = 0; ՐՏidx9 < ՐՏitr9.length; ՐՏidx9++) {
            templ_url = ՐՏitr9[ՐՏidx9];
            ՐՏitr10 = ՐՏ_Iterable(routes_map[templ_url]);
            for (ՐՏidx10 = 0; ՐՏidx10 < ՐՏitr10.length; ՐՏidx10++) {
                spa_route = ՐՏitr10[ՐՏidx10];
                route = spa_route.path;
                if (route.startsWith("/")) {
                    route = route.slice(1);
                }
                if (spa_route.is_main_path) {
                    route = `(${route})?`;
                }
                [type_prefix, component_or_url] = templ_url.split(":");
                rec = {
                    path: `/${route}`,
                    component: new PageWrapper(component_or_url, pages)
                };
                ret.push(rec);
            }
        }
        return ret;
    }
    function make_router(routes_map, pages) {
        var router;
        router = new VueRouter({
            routes: make_routes(routes_map, pages),
            mode: "history",
            base: env.app_base
        });
        return router;
    }
    define([ "amd", "js/axios.min", "js/vue-router" ], function(amd_, axios_, VueRouter_) {
        [amd, axios, VueRouter] = [ amd_, axios_, VueRouter_ ];
        api = new API(axios, env.app_base);
        return {
            load_component: load_component,
            make_router: make_router,
            api: api,
            RSVue: RS_vue,
            v_collector: function() {
                return new V_collector();
            },
            asyncer: asyncer
        };
    });
})();
})();
