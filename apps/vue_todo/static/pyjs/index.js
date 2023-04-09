(function(){
'use strict';
function ϟ_def_modules(){
    var modules;
    modules = {};
    function set_export(prop, get, set){
        var rs_mod, args, mod_id, def_prop;
        rs_mod = this;
        if(Array.isArray(prop)){
            for(args of prop){
                rs_mod.export(...args);
            };
            return;
        };
        if(typeof get === "string"){
            mod_id = get;
            get = () => modules[mod_id];
            set = null;
        };
        def_prop = {
            "configurable": true, 
            "enumerable": true, 
            "get": get
        };
        if(set){
            def_prop["set"] = set;
        };
        Object.defineProperty(rs_mod["exports"], prop, def_prop);
    };
    function def_module(mod_id){
        var rs_mod_id, rs_mod;
        rs_mod_id = `ϟ:${mod_id}`;
        rs_mod = modules[rs_mod_id] = {
            "ϟ_body": () => rs_mod["exports"], 
            "exports": {}, 
            "ϟ_invoked": false
        };
        rs_mod["export"] = set_export;
        function getter(){
            var mod;
            mod = modules[rs_mod_id];
            if(mod["ϟ_invoked"]){
                return mod["exports"];
            };
            mod["ϟ_invoked"] = true;
            return mod["ϟ_body"]()["exports"];
        };
        function setter(v){
            modules[rs_mod_id]["exports"] = v;
        };
        Object.defineProperty(modules, mod_id, {
            "enumerable": true, 
            "get": getter, 
            "set": setter
        });
        return rs_mod;
    };
    Object.defineProperty(modules, "ϟ_defmod", {
        "configurable": false, 
        "enumerable": false, 
        "value": def_module
    });
    return modules;
}
var ϟ_modules = ϟ_def_modules();
var ϟ_defmod = ϟ_modules.ϟ_defmod;
ϟ_defmod("baselib");
ϟ_modules["ϟ:baselib"].ϟ_body = function (){
    var STR_CTR, ARR_CTR, SET_CTR;
    var __name__ = "baselib";
    STR_CTR = "".constructor;
    ARR_CTR = [].constructor;
    SET_CTR = Set.prototype.constructor;
    function is_in(v, obj){
        if(typeof obj.indexOf === "function"){
            return obj.indexOf(v) !== -1;
        }else if(typeof obj.has === "function"){
            return obj.has(v);
        };
        return obj.hasOwnProperty(v);
    };
    function iterable(obj){
        var octr;
        octr = obj.constructor;
        if(octr === STR_CTR || Symbol.iterator in obj){
            return obj;
        };
        return Object.keys(obj);
    };
    function len(obj){
        var octr;
        octr = obj.constructor;
        if(octr === STR_CTR || octr === ARR_CTR){
            return obj.length;
        };
        if(octr === SET_CTR){
            return obj.size;
        };
        return Object.keys(obj).length;
    };
    function type(obj){
        if(obj === null){
            return null;
        };
        return Object.getPrototypeOf(obj).constructor;
    };
    function max(a){
        return Math.max.apply(null, Array.isArray(a) ? a : arguments);
    };
    function min(a){
        return Math.max.apply(null, Array.isArray(a) ? a : arguments);
    };
    function reversed(arr){
        var tmp;
        tmp = arr.slice(0);
        return tmp.reverse();
    };
    function sorted(arr){
        var tmp;
        tmp = arr.slice(0);
        return tmp.sort();
    };
    function hasattr(obj, name){
        return name in obj;
    };
    function *dir(obj){
        var seen, k, v, cur;
        seen = new Set();
        for([k, v] of Object.entries(Object.getOwnPropertyDescriptors(obj))){
            seen.add(k);
            yield [k, v];
        };
        cur = Object.getPrototypeOf(obj);
        while(cur){
            if(cur.constructor && cur.constructor === Object){
                break;
            };
            for([k, v] of Object.entries(Object.getOwnPropertyDescriptors(cur))){
                if(!seen.has(k)){
                    seen.add(k);
                    yield [k, v];
                };
            };
            cur = Object.getPrototypeOf(cur);
        };
    };
    function decor(){
        var args, fun, d;
        args = [...arguments];
        fun = args.pop();
        args.reverse();
        for(d of args){
            fun = d(fun);
        };
        return fun;
    };
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:baselib"];
    Object.assign(ϟ_modules["ϟ:baselib"].exports, {__name__, STR_CTR, ARR_CTR, SET_CTR, is_in, iterable, len, type, max, min, reversed, sorted, hasattr, dir, decor});
    return ϟ_mod;
};
var ϟ_iterable = ϟ_modules["baselib"].iterable;
var type = ϟ_modules["baselib"].type;
var ϟ_in = ϟ_modules["baselib"].is_in;
var len = ϟ_modules["baselib"].len;

ϟ_defmod("main");
ϟ_defmod("asset");
ϟ_defmod("asset.utils");
ϟ_defmod("components");
ϟ_defmod("components.todo");
ϟ_defmod("pyjsaw.pyjs");
ϟ_defmod("pyjsaw.pyjs.vcollector");
ϟ_defmod("asset.server");
ϟ_defmod("asset.asyncer");
ϟ_modules["ϟ:asset"].export("utils", "asset.utils");
ϟ_modules["ϟ:asset"].export("server", "asset.server");
ϟ_modules["ϟ:asset"].export("asyncer", "asset.asyncer");
ϟ_modules["ϟ:components"].export("todo", "components.todo");
ϟ_modules["ϟ:pyjsaw.pyjs"].export("vcollector", "pyjsaw.pyjs.vcollector");
ϟ_modules["ϟ:main"].ϟ_body = function (){
    var __name__ = "main";
    var utils = ϟ_modules["asset"].utils;
    var components = ϟ_modules["components"];
    utils.register_components(Vue, components);
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:main"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["utils", ()=>utils, (v)=>{if (typeof utils !== "undefined") utils = v;}],
        ["components", ()=>components, (v)=>{if (typeof components !== "undefined") components = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:asset"].ϟ_body = function (){
    var __name__ = "asset";
    var utils = ϟ_modules["asset"].utils;
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:asset"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["utils", ()=>utils, (v)=>{if (typeof utils !== "undefined") utils = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:asset.utils"].ϟ_body = function (){
    var __name__ = "asset.utils";
    function register_components(Vue, components_pkg){
        var module_name, module, c, cid, ϟ_1;
        if(!components_pkg){
            return;
        };
        for(module_name of ϟ_iterable(components_pkg)){
            if(module_name.startsWith("__")){
                continue;
            };
            module = components_pkg[module_name];
            c = module.make();
            cid = (ϟ_1 = c.name.split("."))[ϟ_1.length - 1];
            Vue.component(cid, c);
        };
    };
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:asset.utils"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["register_components", ()=>register_components, (v)=>{if (typeof register_components !== "undefined") register_components = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:components"].ϟ_body = function (){
    var __name__ = "components";
    var todo = ϟ_modules["components"].todo;
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:components"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["todo", ()=>todo, (v)=>{if (typeof todo !== "undefined") todo = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:components.todo"].ϟ_body = function (){
    var ENV, srv_api, templ, ϟ_1, ϟ_2, ϟ_3, ϟ_4, ϟ_5, ϟ_6;
    var __name__ = "components.todo";
    var vc = ϟ_modules["pyjsaw.pyjs.vcollector"].vc;
    var API = ϟ_modules["asset.server"].API;
    var asyncer = ϟ_modules["asset.asyncer"].asyncer;
    ENV = window.WEBSAW_ENV;
    srv_api = new API(axios, ENV.app_base);
    templ = '<div><h1>TODO</h1><div v-for="it in items" v-bind:key="it.id"><span>id:{{it.id}}</span><input v-model="it.item" v-on:change="update(it.id)"/><button v-on:click="remove(it.id)">Remove</button></div><div><input v-model="new_item" v-on:changed="insert"/><button v-on:click="insert">Add</button></div></div>';
    ϟ_1 = vc.component();
    class Todo{
        get __class__(){
            return this.constructor;
        };
        static template = templ;
        static api = [String, ""];
        static todos = [Object, null];
        data(vm){
            var data_obj;
            data_obj = this;
            data_obj.new_item = null;
            data_obj.items = {
                ...vm.todos
            };
        };
        *reload(){
            var self, resp;
            self = this;
            resp = yield srv_api.get(self.api);
            self.items = resp.data.items;
        };
        *insert(){
            var self, resp;
            self = this;
            resp = yield srv_api.post(self.api, {
                "item": self.new_item
            });
            self.items = resp.data.items;
        };
        *update(id){
            var self, resp;
            self = this;
            resp = yield srv_api.post([self.api, id], {
                "item": self.items[id].item
            });
            self.items = resp.data.items;
        };
        *remove(id){
            var self, resp;
            self = this;
            resp = yield srv_api.delete([self.api, id]);
            self.items = resp.data.items;
        };
    };
    Todo.prototype.reload = (ϟ_2=asyncer(Todo.prototype.reload), ϟ_2);
    Todo.prototype.insert = (ϟ_3=asyncer(Todo.prototype.insert), ϟ_3);
    Todo.prototype.update = (ϟ_4=asyncer(Todo.prototype.update), ϟ_4);
    Todo.prototype.remove = (ϟ_5=asyncer(Todo.prototype.remove), ϟ_5);
    Todo = (ϟ_6=ϟ_1(Todo), ϟ_6);

    function make(){
        return Todo;
    };
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:components.todo"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["vc", ()=>vc, (v)=>{if (typeof vc !== "undefined") vc = v;}],
        ["API", ()=>API, (v)=>{if (typeof API !== "undefined") API = v;}],
        ["asyncer", ()=>asyncer, (v)=>{if (typeof asyncer !== "undefined") asyncer = v;}],
        ["ENV", ()=>ENV, (v)=>{if (typeof ENV !== "undefined") ENV = v;}],
        ["srv_api", ()=>srv_api, (v)=>{if (typeof srv_api !== "undefined") srv_api = v;}],
        ["templ", ()=>templ, (v)=>{if (typeof templ !== "undefined") templ = v;}],
        ["Todo", ()=>Todo, (v)=>{if (typeof Todo !== "undefined") Todo = v;}],
        ["make", ()=>make, (v)=>{if (typeof make !== "undefined") make = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:pyjsaw.pyjs"].ϟ_body = function (){
    var __name__ = "pyjsaw.pyjs";
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:pyjsaw.pyjs"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:pyjsaw.pyjs.vcollector"].ϟ_body = function (){
    var _SPECIAL_VUEMETHODS, vc, __all__;
    var __name__ = "pyjsaw.pyjs.vcollector";
    _SPECIAL_VUEMETHODS = new Set(["beforeCreate", "created", "beforeMount", "mounted", "beforeUpdate", "updated", "activated", "deactivated", "beforeDestroy", "destroyed", "render"]);
    function is_hook(name){
        return _SPECIAL_VUEMETHODS.has(name);
    };
    function is_special(name){
        return (new RegExp("^((_.+)|constructor)$")).test(name);
    };
    function vopt_from_class(cls){
        var v_collector, vcd, bases, data_setup, meth_name, v, prop_name, prop, prop_, keys, ϟ_1, i, ret, c;
        v_collector = cls.__vue_opt__;
        vcd = {};
        vcd.name = cls.name;
        vcd.props = {};
        vcd.methods = {};
        if(v_collector){
            bases = v_collector.bases;
            if(bases && bases.length){
                vcd.mixins = v_collector.bases;
            };
            vcd.computed = v_collector._computed;
            vcd.directives = v_collector._directives;
            vcd.filters = v_collector._filters;
            vcd.watch = v_collector._watch;
        };
        data_setup = cls.prototype.data;
        if(data_setup){
            function data(){
                var data_obj;
                data_obj = {};
                data_setup.call(data_obj, this);
                return data_obj;
            };
            vcd.data = data;
        };
        for([meth_name, v] of Object.entries(Object.getOwnPropertyDescriptors(cls.prototype))){
            if(meth_name === "data" || is_special(meth_name) || v_collector && v_collector.__collected__[meth_name] || !v.value){
                continue;
            };
            if(is_hook(meth_name)){
                vcd[meth_name] = v.value;
            }else{
                vcd.methods[meth_name] = v.value;
            };
        };
        for(prop_name in cls){
            if(prop_name === "_extra" || prop_name.startsWith("__")){
                continue;
            };
            if(prop_name === "template" && typeof cls[prop_name] === "string"){
                vcd[prop_name] = cls[prop_name];
            }else{
                prop = cls[prop_name];
                if(Array.isArray(prop)){
                    prop_ = {};
                    keys = ["type", "default", "required", "validator"];
                    ϟ_1 = 0;
                    for(v of prop){
                        i = ϟ_1++;
                        if(v === undefined){
                            continue;
                        };
                        prop_[keys[i]] = v;
                    };
                    prop = prop_;
                };
                vcd.props[prop_name] = prop;
            };
        };
        if("_extra" in cls){
            Object.assign(vcd, cls["_extra"]);
        };
        if("_postproc" in cls){
            ret = cls["_postproc"](vcd);
            if(ret){
                vcd = ret;
            };
        };
        if(Array.isArray(vcd.components)){
            vcd.components = (() => {var ϟ_2 = {}; for(c of vcd.components){ϟ_2[c.name] = c;}; return ϟ_2})();
        };
        return vcd;
    };
    class VCollector{
        get __class__(){
            return this.constructor;
        };
        constructor(){
            var self;
            self = this;
            self._methods = null;
            self._computed = null;
            self._watch = null;
            self._filters = null;
            self._directives = null;
            self.__current__ = null;
            self.__collected__ = {};
        };
        _collector(opt_name, extra){
            var self;
            self = this;
            self.__current__ = {
                "__collected__": {}
            };
            if(extra){
                Object.assign(self.__current__, extra);
            };
            function wrapper(cls){
                cls[opt_name] = self.__current__;
                self.__current__ = null;
                return vopt_from_class(cls);
            };
            return wrapper;
        };
        component(){
            var self, bases;
            self = this;
            bases = [...arguments];
            return self._collector("__vue_opt__", {
                "bases": bases
            });
        };
        _reg_as(reg_as, name, fun_opt){
            var self, cur, computed, fun;
            self = this;
            cur = self.__current__;
            if(!cur[reg_as]){
                cur[reg_as] = {};
            }else if(reg_as === "_computed"){
                computed = cur[reg_as];
                if(computed[name]){
                    computed[name] = {
                        "get": computed[name], 
                        "set": fun_opt
                    };
                    return fun_opt;
                };
            };
            cur[reg_as][name] = fun_opt;
            fun = (fun_opt.handler) ? fun_opt.handler : fun_opt;
            cur.__collected__[fun.name] = true;
            return fun;
        };
        computed(fun){
            var self, fun_name;
            self = this;
            fun_name = fun.__name__ || fun.name;
            if(fun_name.startsWith("get ") || fun_name.startsWith("set ")){
                fun_name = fun_name.slice(4);
            };
            return self._reg_as("_computed", fun_name, fun);
        };
        filter(fun){
            var self, fun_name;
            self = this;
            fun_name = fun.__name__ || fun.name;
            return self._reg_as("_filters", fun_name, fun);
        };
        directive(fun){
            var self, fun_name;
            self = this;
            fun_name = fun.__name__ || fun.name;
            return self._reg_as("_directives", fun_name, fun);
        };
        watch(name, opt){
            var self;
            self = this;
            if(!opt){
                opt = {};
            };
            function wrapper(fun){
                opt.handler = fun;
                return self._reg_as("_watch", name, opt);
            };
            return wrapper;
        };
    };

    vc = new VCollector();
    __all__ = [VCollector, vc];
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:pyjsaw.pyjs.vcollector"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["VCollector", ()=>VCollector, (v)=>{if (typeof VCollector !== "undefined") VCollector = v;}],
        ["vc", ()=>vc, (v)=>{if (typeof vc !== "undefined") vc = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:asset.server"].ϟ_body = function (){
    var HTTP_METHODS, ϟ_1;
    var __name__ = "asset.server";
    HTTP_METHODS = "get post put patch delete head".split(" ");
    function _make_meth(meth_name){
        function meth(){
            var args;
            args = [...arguments];
            return this._http(meth_name, ...args);
        };
        return meth;
    };
    function _inject_http_methods(cls){
        var m;
        
        for(m of HTTP_METHODS){
            cls.prototype["_" + m] = _make_meth(m);
        };
        return cls;
    };
    class API{
        get __class__(){
            return this.constructor;
        };
        constructor(axios, baseURL, axios_opt){
            var self, m;
            self = this;
            self.headers_getter = () => ({});
            self.baseURL = baseURL;
            axios_opt = axios_opt || {};
            self.srv = axios.create(axios_opt);
            self.http = self._http.bind(self);
            for(m of ϟ_iterable(HTTP_METHODS)){
                self[m] = self["_" + m].bind(self);
            };
        };
        _http(meth, path_query, data_or_get_headers, headers){
            var self, query, path, data, conf;
            self = this;
            meth = meth.toLowerCase();
            query = null;
            if(type(path_query) === String){
                path = path_query;
            }else{
                if(type(path_query[path_query.length - 1]) === Object){
                    query = path_query.pop();
                };
                path = path_query.join("/");
            };
            if(ϟ_in(meth, ["get", "head"])){
                data = null;
                if(headers === undefined){
                    headers = data_or_get_headers;
                };
            }else{
                data = data_or_get_headers;
            };
            if(!path.startsWith("/")){
                path = `${self.baseURL}/${path}`;
            };
            conf = {
                "method": meth, 
                "url": path
            };
            if(query && len(query)){
                conf.params = query;
            };
            if(data){
                conf.data = data;
            };
            if(headers && len(headers)){
                conf.headers = Object.assign({}, headers, self.headers_getter(conf));
            }else{
                conf.headers = self.headers_getter(conf);
            };
            conf.maxRedirects = 0;
            return self.srv.request(conf);
        };
    };
    API = (ϟ_1=_inject_http_methods(API), ϟ_1);

    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:asset.server"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["HTTP_METHODS", ()=>HTTP_METHODS, (v)=>{if (typeof HTTP_METHODS !== "undefined") HTTP_METHODS = v;}],
        ["_make_meth", ()=>_make_meth, (v)=>{if (typeof _make_meth !== "undefined") _make_meth = v;}],
        ["_inject_http_methods", ()=>_inject_http_methods, (v)=>{if (typeof _inject_http_methods !== "undefined") _inject_http_methods = v;}],
        ["API", ()=>API, (v)=>{if (typeof API !== "undefined") API = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:asset.asyncer"].ϟ_body = function (){
    var __name__ = "asset.asyncer";
    class MergeCall{
        get __class__(){
            return this.constructor;
        };
        set_key(a){
            var self;
            self = this;
            self.cmd = "set_key";
            self.args = a;
            return self;
        };
        merge(a){
            var self;
            self = this;
            self.cmd = "merge";
            self.args = a;
            return self;
        };
    };

    class AsyncerError extends Error{
        get __class__(){
            return this.constructor;
        };
        constructor(msg, fun){
            var self;
            super(msg);
            self = this;
            self.wrapped = fun;
        };
    };

    function asyncer(fun){
        var merge_call;
        merge_call = {};
        function wrap(ctx){
            function pret(ok, err){
                function inner(f, opt){
                    var ret_v, ret_throw, merge_key, v, fname, p;
                    if(opt){
                        ret_v = opt.ret_v;
                        ret_throw = opt.ret_throw;
                        merge_key = opt.merge_key;
                    };
                    function _err(e, merge_key){
                        try{
                            throw e;
                        }catch(ϟException){
                            var e = ϟException;
                            err(e);
                        };
                        if(merge_key){
                            merge_call[merge_key].map((cb) => cb.err(e));
                            delete merge_call[merge_key];
                        };
                    };
                    if(ret_throw){
                        v = ret_throw;
                    }else{
                        try{
                            if(!f){
                                f = fun.apply(ctx.self, ctx.args);
                                if(!(f && f.next)){
                                    fname = fun.__name__ || fun.name || "<anonymous>";
                                    throw new AsyncerError(`${fname} must be instance of Generator`, fun);
                                };
                            };
                            v = f.next(ret_v);
                        }catch(ϟException){
                            var e = ϟException;
                            _err(e, merge_key);
                            return;
                        };
                    };
                    function resolve_cb(ret_v){
                        inner(f, {
                            "ret_v": ret_v, 
                            "merge_key": merge_key
                        });
                    };
                    function reject_cb(e){
                        var v;
                        try{
                            v = f.throw(e);
                        }catch(ϟException){
                            var e = ϟException;
                            _err(e, merge_key);
                            return;
                        };
                        inner(f, {
                            "ret_throw": v, 
                            "merge_key": merge_key
                        });
                    };
                    if(v.value instanceof MergeCall){
                        if(v.value.cmd === "get_keys"){
                            Promise.resolve(Object.keys(merge_call)).then(resolve_cb);
                        }else if(v.value.cmd === "merge"){
                            p = merge_call[v.value.args];
                            if(p){
                                p.push({
                                    "ok": (v) => ok(v), 
                                    "err": (v) => err(v)
                                });
                                return;
                            }else{
                                merge_key = v.value.args;
                                merge_call[merge_key] = [];
                                Promise.resolve(null).then(resolve_cb);
                            };
                        }else{
                            Promise.resolve(null).then(resolve_cb);
                        };
                    }else if(!v.done){
                        if(v.value instanceof Promise){
                            v.value.then(resolve_cb, reject_cb);
                        }else{
                            Promise.resolve(v.value).then(resolve_cb);
                        };
                    }else{
                        ok(v.value);
                        if(merge_key){
                            merge_call[merge_key].map((cb) => cb.ok(v.value));
                            delete merge_call[merge_key];
                        };
                    };
                };
                inner();
            };
            return pret;
        };
        function ret(){
            var ctx, p;
            ctx = {
                "self": this, 
                "args": arguments
            };
            p = new Promise(wrap(ctx));
            return p;
        };
        ret.__name__ = fun.__name__ || fun.name;
        return ret;
    };
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:asset.asyncer"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["MergeCall", ()=>MergeCall, (v)=>{if (typeof MergeCall !== "undefined") MergeCall = v;}],
        ["AsyncerError", ()=>AsyncerError, (v)=>{if (typeof AsyncerError !== "undefined") AsyncerError = v;}],
        ["asyncer", ()=>asyncer, (v)=>{if (typeof asyncer !== "undefined") asyncer = v;}]
    ]);
    return ϟ_mod;
};
(function (){
    var __name__ = "__main__";
    function _init_(){
        var params, WEBSAW_ENV;
        params = document.getElementsByTagName("meta")[0].dataset;
        WEBSAW_ENV = window.WEBSAW_ENV = Object.assign({}, params);
        WEBSAW_ENV.app_static = WEBSAW_ENV.app_base + "/static";
        var main = ϟ_modules["main"];
    };
    _init_();
})()
})()