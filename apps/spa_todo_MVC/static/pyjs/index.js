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

ϟ_defmod("app");
ϟ_defmod("pyjsaw.pyjs");
ϟ_defmod("pyjsaw.pyjs.vcollector");
ϟ_defmod("asset");
ϟ_defmod("asset.spa_bundle");
ϟ_defmod("asset.spa_tools");
ϟ_defmod("asset.asyncer");
ϟ_defmod("asset.server");
ϟ_defmod("components");
ϟ_defmod("pages");
ϟ_defmod("pages.todo");
ϟ_defmod("store");
ϟ_defmod("store.AppStore");
ϟ_modules["ϟ:pyjsaw.pyjs"].export("vcollector", "pyjsaw.pyjs.vcollector");
ϟ_modules["ϟ:asset"].export("spa_bundle", "asset.spa_bundle");
ϟ_modules["ϟ:asset"].export("asyncer", "asset.asyncer");
ϟ_modules["ϟ:asset"].export("server", "asset.server");
ϟ_modules["ϟ:asset"].export("spa_tools", "asset.spa_tools");
ϟ_modules["ϟ:pages"].export("todo", "pages.todo");
ϟ_modules["ϟ:store"].export("AppStore", "store.AppStore");
ϟ_modules["ϟ:app"].ϟ_body = function (){
    var store, ϟ_1, ϟ_2, app, __all__;
    var __name__ = "app";
    var vc = ϟ_modules["pyjsaw.pyjs.vcollector"].vc;
    var spa_bundle = ϟ_modules["asset"].spa_bundle;
    var spa_tools = ϟ_modules["asset"].spa_tools;
    var components = ϟ_modules["components"];
    var pages = ϟ_modules["pages"];
    var AppStore = ϟ_modules["store"].AppStore;
    spa_bundle.register_components(Vue, components);
    store = new AppStore();
    Vue.prototype.$store = store;
    spa_tools.PageUtil.set_headers_getter(() => ({
        "x-api-token": store.get("api_token")
    }));
    Vue.mixin(spa_tools.PageUtil.vue_mixin());
    ϟ_1 = vc.component();
    class App{
        get __class__(){
            return this.constructor;
        };
        render(h){
            var self;
            self = this;
            return h("router-view");
        };
        static _extra = {
            router: spa_tools.make_router(SPA_ROUTES, pages)
        };
    };
    App = (ϟ_2=ϟ_1(App), ϟ_2);

    Vue.use(VueRouter);
    function auth_guard(dst, src, next){
        if(dst.meta === "requires_login" && !store.get("user").name){
            next({
                "path": "/login", 
                "query": {
                    "next": dst.fullPath
                }
            });
        }else{
            next();
        };
    };
    App.router.beforeEach(auth_guard);
    App.router.beforeEach(spa_tools.data_preloader_guard);
    app = window.app = new Vue(App);
    __all__ = [app];
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:app"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["app", ()=>app, (v)=>{if (typeof app !== "undefined") app = v;}]
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

 ϟ_modules["ϟ:asset"].ϟ_body = function (){
    var __name__ = "asset";
    var spa_bundle = ϟ_modules["asset"].spa_bundle;
    var spa_tools = ϟ_modules["asset"].spa_tools;
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:asset"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["spa_bundle", ()=>spa_bundle, (v)=>{if (typeof spa_bundle !== "undefined") spa_bundle = v;}],
        ["spa_tools", ()=>spa_tools, (v)=>{if (typeof spa_tools !== "undefined") spa_tools = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:asset.spa_bundle"].ϟ_body = function (){
    var __name__ = "asset.spa_bundle";
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
    var ϟ_mod = ϟ_modules["ϟ:asset.spa_bundle"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["register_components", ()=>register_components, (v)=>{if (typeof register_components !== "undefined") register_components = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:asset.spa_tools"].ϟ_body = function (){
    var ENV, PAGES_API, router, api, ϟ_1, ϟ_2, page_mixin, ϟ_4, data_preloader, ϟ_5;
    var __name__ = "asset.spa_tools";
    var asyncer = ϟ_modules["asset.asyncer"].asyncer;
    var API = ϟ_modules["asset.server"].API;
    ENV = window.SPA_ENV;
    PAGES_API = `pages-api/${ENV.spa_name}`;
    router = null;
    api = new API(axios, ENV.app_base);
    class PageUtil{
        get __class__(){
            return this.constructor;
        };
        static set_headers_getter(hg){
            api.headers_getter = hg;
        };
        constructor(vm){
            var self;
            self = this;
            self.vm = vm;
            self.on_mounted_enabled = false;
        };
        get page_api(){
            var self;
            self = this;
            return `${PAGES_API}${self.vm.$route.path}`;
        };
        get page_vm(){
            var self, route;
            self = this;
            route = self.vm.$route.matched[0];
            if(route){
                return route.instances.default.$children[0];
            };
            return null;
        };
        *http(meth, path_query, data_or_get_headers, headers){
            var self, resp;
            self = this;
            if(!path_query || !len(path_query)){
                path_query = [self.page_api];
            }else{
                if(!(path_query instanceof Array)){
                    path_query = [path_query];
                };
                if(len(path_query) === 1 && type(path_query[0]) !== String){
                    path_query = [null, path_query[0]];
                };
                if(!path_query[0]){
                    path_query[0] = self.page_api;
                }else if(!(new RegExp("^(pages-api|/)")).exec(path_query[0])){
                    path_query[0] = `${PAGES_API}/${path_query[0]}`;
                };
            };
            resp = yield api.http(meth, path_query, data_or_get_headers, headers);
            if(self._on_response){
                self._on_reponse.call(null, resp);
            }else{
                self.vm.on_response(resp);
            };
        };
        get(){
            var self, args, len_args, path, query, headers;
            self = this;
            args = [...arguments];
            len_args = len(args);
            [path, query, headers] = [null, null, null];
            if(len_args === 1){
                path = args.pop();
            }else if(len_args === 2){
                [path, query] = args;
            }else if(len_args === 3){
                [path, query, headers] = args;
            };
            return self.http("get", [path, query], headers);
        };
        post(){
            var self, args;
            self = this;
            args = [...arguments];
            return self.http("post", ...args);
        };
        remove(){
            var self, args;
            self = this;
            args = [...arguments];
            return self.http("delete", ...args);
        };
        *redirect(path, query){
            var self;
            self = this;
            if(query === undefined && type(path) === Object){
                query = path;
                path = null;
            };
            if(!path || path === "."){
                path = self.vm.$route.path;
            };
            if(path[0] !== "/"){
                path = "/" + path;
            };
            if(!query){
                query = {};
            };
            try{
                yield self.vm.$router.push({
                    "path": path, 
                    "query": query
                });
            }catch(ϟException){
                var err = ϟException;
                if(err._isRouter && err.type !== VueRouter.NavigationFailureType.duplicated){
                    throw ϟException;
                };
                self.reload_data();
            };
        };
        reload_data(){
            var self, r;
            self = this;
            r = self.vm.$route;
            self.get("." + r.path, r.query);
        };
        parse_response(r){
            var self, payload, commands, state_patch, set_state, data;
            self = this;
            payload = r.data || {};
            commands = null;
            state_patch = null;
            set_state = null;
            if(r.headers["x-sparesponse"]){
                data = payload.data || {};
                state_patch = payload.state_patch || null;
                set_state = payload.set_state || null;
                delete payload.data;
                delete payload.state_patch;
                delete payload.set_state;
                commands = payload;
            }else{
                data = payload;
            };
            return {
                "data": data, 
                "commands": commands, 
                "state_patch": state_patch, 
                "set_state": set_state
            };
        };
        apply_response(vm, r){
            var self, back, store, set_state, it, k, c, args;
            self = this;
            back = self.parse_response(r);
            store = vm.$store;
            if(back.state_patch){
                store.update(back.state_patch);
            };
            if(back.set_state){
                set_state = back.set_state;
                if(!Array.isArray(set_state[0])){
                    set_state = [set_state];
                };
                for(it of ϟ_iterable(set_state)){
                    store.set(...it);
                };
            };
            for(k of ϟ_iterable(back.data)){
                vm[k] = back.data[k];
            };
            for(c of ϟ_iterable(back.commands || [])){
                args = back.commands[c];
                if(!Array.isArray(args)){
                    args = [args];
                };
                vm[c].call(vm, ...args);
            };
        };
        on_mounted(){
            var self, vm, back, store, set_state, it, c, args;
            self = this;
            vm = self.vm;
            if(!self.on_mounted_enabled){
                return;
            };
            back = vm.$back;
            store = vm.$store;
            if(back.state_patch){
                store.update(back.state_patch);
            };
            if(back.set_state){
                set_state = back.set_state;
                if(!Array.isArray(set_state[0])){
                    set_state = [set_state];
                };
                for(it of ϟ_iterable(set_state)){
                    store.set(...it);
                };
            };
            for(c of ϟ_iterable(back.commands || [])){
                args = back.commands[c];
                if(!Array.isArray(args)){
                    args = [args];
                };
                vm[c].call(vm, ...args);
            };
        };
        on_response(r){
            var self;
            self = this;
            self.apply_response(self.vm, r);
        };
        static vue_mixin(){
            function on_response(r){
                var vm;
                vm = this;
                vm.$pu.on_response(r);
            };
            function beforeCreate(){
                var vm, meths;
                vm = this;
                vm.$pu = new PageUtil(vm);
                meths = vm.$options.methods;
                console.log("create:", meths);
                if(!meths){
                    meths = vm.$options.methods = {};
                };
                if(!("on_response" in meths)){
                    meths["on_response"] = on_response;
                };
            };
            return {
                "beforeCreate": beforeCreate
            };
        };
    };
    PageUtil.prototype.http = (ϟ_1=asyncer(PageUtil.prototype.http), ϟ_1);
    PageUtil.prototype.redirect = (ϟ_2=asyncer(PageUtil.prototype.redirect), ϟ_2);

    page_mixin = {
        beforeCreate: function (){
            var self;
            self = this;
            self.$back = self.$pu.parse_response(self.$attrs.pg_response);
        }, 
        data: function (){
            var self;
            self = this;
            self.$pu.on_mounted_enabled = true;
            return self.$back.data;
        }, 
        methods: {
            redirect: function (){
                var self, args;
                self = this;
                args = [...arguments];
                self.$pu.redirect(...args);
            }, 
            alert: function (msg){
                var self, ϟ_3;
                self = this;
                function _(){
                    setTimeout(() => alert(msg), 100);
                };
                _ = (ϟ_3=self.$nextTick(_), ϟ_3);
            }
        }, 
        watch: {
            S_route: function (to_, from_){
                var self, page_url;
                self = this;
                page_url = to_.path.slice(1);
                self.$pu.get(page_url, to_.query);
            }
        }, 
        computed: {
            page_api: function (){
                var self;
                self = this;
                return self.$pu.page_api;
            }, 
            page_api_root: function (){
                var self;
                self = this;
                return PAGES_API;
            }
        }, 
        mounted: function (){
            var self;
            self = this;
            self.$pu.on_mounted();
        }
    };
    class DataPreloader{
        get __class__(){
            return this.constructor;
        };
        constructor(){
            var self;
            self = this;
            self.response = null;
            self.page_uri = null;
            self._dest_route = null;
        };
        get dest_route(){
            var self, ret;
            self = this;
            ret = self._dest_route;
            self._dest_route = null;
            return ret;
        };
        *preload(dest_route){
            var self, page_api_uri;
            self = this;
            self._dest_route = dest_route;
            page_api_uri = self.page_uri = PAGES_API + dest_route.fullPath;
            self.response = null;
            self.response = yield api.get([page_api_uri]);
        };
    };
    DataPreloader.prototype.preload = (ϟ_4=asyncer(DataPreloader.prototype.preload), ϟ_4);

    data_preloader = new DataPreloader();
    function make_loader(page_component, pages){
        function load_page(ok, err){
            var pg_module, component, wrapper;
            pg_module = pages[page_component];
            component = pg_module.make();
            component.mixins = [page_mixin];
            wrapper = {
                functional: true, 
                render: function (h, ctx){
                    if(!ctx.data.attrs){
                        ctx.data.attrs = {};
                    };
                    ctx.data.attrs.pg_response = data_preloader.response;
                    return h(component, ctx.data, ctx.children);
                }
            };
            ok(wrapper);
        };
        return load_page;
    };
    function make_routes(routes_map, pages){
        var ret, templ_url, spa_route, route, type_prefix, page_component, rec;
        ret = [];
        for(templ_url of ϟ_iterable(routes_map)){
            for(spa_route of ϟ_iterable(routes_map[templ_url])){
                route = spa_route.path;
                if(route.startsWith("/")){
                    route = route.slice(1);
                };
                if(spa_route.is_main_path){
                    route = `(${route})?`;
                };
                [type_prefix, page_component] = templ_url.split(":");
                rec = {
                    "path": `/${route}`, 
                    "meta": spa_route.meta, 
                    "component": make_loader(page_component, pages)
                };
                ret.push(rec);
            };
        };
        return ret;
    };
    function *data_preloader_guard(dest, cur, next){
        yield data_preloader.preload(dest);
        next();
    };
    data_preloader_guard = (ϟ_5=asyncer(data_preloader_guard), ϟ_5);
    function make_router(routes_map, pages){
        var router;
        router = new VueRouter({
            "routes": make_routes(routes_map, pages), 
            "mode": "history", 
            "base": ENV.app_base
        });
        return router;
    };
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:asset.spa_tools"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["asyncer", ()=>asyncer, (v)=>{if (typeof asyncer !== "undefined") asyncer = v;}],
        ["API", ()=>API, (v)=>{if (typeof API !== "undefined") API = v;}],
        ["ENV", ()=>ENV, (v)=>{if (typeof ENV !== "undefined") ENV = v;}],
        ["PAGES_API", ()=>PAGES_API, (v)=>{if (typeof PAGES_API !== "undefined") PAGES_API = v;}],
        ["router", ()=>router, (v)=>{if (typeof router !== "undefined") router = v;}],
        ["api", ()=>api, (v)=>{if (typeof api !== "undefined") api = v;}],
        ["PageUtil", ()=>PageUtil, (v)=>{if (typeof PageUtil !== "undefined") PageUtil = v;}],
        ["page_mixin", ()=>page_mixin, (v)=>{if (typeof page_mixin !== "undefined") page_mixin = v;}],
        ["DataPreloader", ()=>DataPreloader, (v)=>{if (typeof DataPreloader !== "undefined") DataPreloader = v;}],
        ["data_preloader", ()=>data_preloader, (v)=>{if (typeof data_preloader !== "undefined") data_preloader = v;}],
        ["make_loader", ()=>make_loader, (v)=>{if (typeof make_loader !== "undefined") make_loader = v;}],
        ["make_routes", ()=>make_routes, (v)=>{if (typeof make_routes !== "undefined") make_routes = v;}],
        ["data_preloader_guard", ()=>data_preloader_guard, (v)=>{if (typeof data_preloader_guard !== "undefined") data_preloader_guard = v;}],
        ["make_router", ()=>make_router, (v)=>{if (typeof make_router !== "undefined") make_router = v;}]
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

 ϟ_modules["ϟ:components"].ϟ_body = function (){
    var __name__ = "components";
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:components"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:pages"].ϟ_body = function (){
    var __name__ = "pages";
    var todo = ϟ_modules["pages"].todo;
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:pages"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["todo", ()=>todo, (v)=>{if (typeof todo !== "undefined") todo = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:pages.todo"].ϟ_body = function (){
    var templ, STORAGE_KEY, ϟ_1, ϟ_2, ϟ_3, ϟ_4, ϟ_5;
    var __name__ = "pages.todo";
    var vc = ϟ_modules["pyjsaw.pyjs.vcollector"].vc;
    templ = '<div><section class="todoapp"><header class="header"><h1>Todos</h1><input v-on:keyup.enter="addTodo" autofous="autofocus" placeholder="What needs to be done?" class="new-todo"/></header><section v-show="todos.length" class="main"><input v-bind:checked="remaining == 0" v-on:change="toggleAll" id="toggle-all" class="toggle-all" type="checkbox"/><label For="toggle-all">Mart all as complete</label><ul class="todo-list"><li v-for="todo in filteredTodos" v-bind:key="todo.id" v-bind:class="{ completed: todo.completed, editing: todo == editedTodo }" class="todo"><div class="view"><input v-model="todo.completed" type="checkbox" class="toggle"/><label v-on:dblclick="editTodo(todo)">{{todo.title}}</label><button v-on:click="removeTodo(todo)" class="destroy"></button></div><input v-model="todo.title" v-if="todo == editedTodo" v-on:vnode-mounted="el.focus()" v-on:keyup.enter="doneEdit(todo)" v-on:keyup.escape="cancelEdit(todo)" v-on:blur="doneEdit(todo)" class="edit" Type="text"/></li></ul></section><footer v-show="todos.length" class="footer"><span class="todo-count">{{remaining}} {{ remaining == 1 ? " item" : " items"  }} left</span><ul class="filters"><li><a v-bind:class="{ selected: visibility == \'all\' }" href="#/all">All</a></li><li><a v-bind:class="{ selected: visibility == \'active\' }" href="#/active">Active</a></li><li><a v-bind:class="{ selected: visibility == \'completed\' }" href="#/completed">Completed</a></li><button v-on:click="removeCompleted" v-show="todos.length > remaining" class="clear-completed">Clear completed</button></ul></footer></section></div>';
    "\nconst filters = {\n  all: (todos) => todos,\n  active: (todos) => todos.filter((todo) => !todo.completed),\n  completed: (todos) => todos.filter((todo) => todo.completed)\n}\n";
    function filter(data, key){
        var filtered, rec;
        filtered = [];
        if(key === "all"){
            return data;
        };
        if(key === "active"){
            for(rec of ϟ_iterable(data)){
                if(rec["completed"] === false){
                    filtered.push(rec);
                };
            };
            return filtered;
        };
        if(key === "completed"){
            for(rec of ϟ_iterable(data)){
                if(rec["completed"] === true){
                    filtered.push(rec);
                };
            };
            return filtered;
        };
    };
    STORAGE_KEY = "spa_todo_mvc";
    ϟ_1 = vc.component();
    class Todo{
        get __class__(){
            return this.constructor;
        };
        static template = templ;
        data(vm){
            var data_obj;
            data_obj = this;
            data_obj.todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
            data_obj.editedTodo = null;
            data_obj.visibility = "all";
        };
        todos(n, o){
            var self;
            self = this;
            localStorage.setItem(STORAGE_KEY, JSON.stringify(n));
        };
        mounted(){
            var self;
            self = this;
            window.addEventListener("hashchange", self.onHashChange);
            self.onHashChange();
        };
        filteredTodos(){
            var self;
            self = this;
            return filter(self.todos, self.visibility);
        };
        remaining(){
            var self, data, filtered;
            self = this;
            data = self.todos;
            filtered = filter(data, "active");
            if(filtered){
                return filtered.length;
            }else{
                return 0;
            };
        };
        toggleAll(e){
            var self, todos, t;
            self = this;
            todos = self.todos;
            for(t of ϟ_iterable(todos)){
                t.completed = e.target.checked;
            };
        };
        addTodo(e){
            var self, value;
            self = this;
            value = e.target.value.trim();
            if(!value){
                return;
            };
            self.todos.push({
                "id": Date.now(), 
                "title": value, 
                "completed": false
            });
            e.target.value = "";
        };
        removeTodo(todo){
            var self;
            self = this;
            self.todos.splice(self.todos.indexOf(todo), 1);
        };
        editTodo(todo){
            var self;
            self = this;
            self.beforeEditCache = todo.title;
            self.editedTodo = todo;
        };
        doneEdit(todo){
            var self;
            self = this;
            if(!self.editedTodo){
                return;
            };
            self.editedTodo = null;
            todo.title = todo.title.trim();
            if(!todo.title){
                self.removeTodo(todo);
            };
        };
        removeCompleted(){
            var self, data;
            self = this;
            data = self.todos;
            self.todos = filter(data, "active");
        };
        cancelEdit(todo){
            var self;
            self = this;
            self.editedTodo = null;
            todo.title = self.beforeEditCache;
        };
        onHashChange(){
            var self, visibility, data;
            self = this;
            visibility = window.location.hash.replace(new RegExp("#/?"), "");
            data = filter(self.todos, visibility);
            if(data){
                self.visibility = visibility;
            }else{
                window.location.hash = "";
                self.visibility = "all";
            };
        };
    };
    Todo.prototype.todos = (ϟ_2=vc.watch("todos")(Todo.prototype.todos), ϟ_2);
    Todo.prototype.filteredTodos = (ϟ_3=vc.computed(Todo.prototype.filteredTodos), ϟ_3);
    Todo.prototype.remaining = (ϟ_4=vc.computed(Todo.prototype.remaining), ϟ_4);
    Todo = (ϟ_5=ϟ_1(Todo), ϟ_5);

    function make(){
        return Todo;
    };
    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:pages.todo"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["vc", ()=>vc, (v)=>{if (typeof vc !== "undefined") vc = v;}],
        ["templ", ()=>templ, (v)=>{if (typeof templ !== "undefined") templ = v;}],
        ["filter", ()=>filter, (v)=>{if (typeof filter !== "undefined") filter = v;}],
        ["STORAGE_KEY", ()=>STORAGE_KEY, (v)=>{if (typeof STORAGE_KEY !== "undefined") STORAGE_KEY = v;}],
        ["Todo", ()=>Todo, (v)=>{if (typeof Todo !== "undefined") Todo = v;}],
        ["make", ()=>make, (v)=>{if (typeof make !== "undefined") make = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:store"].ϟ_body = function (){
    var __name__ = "store";
    function _make_state(){
        return {
            "st": JSON.parse(SPA_ENV.app_state)
        };
    };
    class AppStore{
        get __class__(){
            return this.constructor;
        };
        constructor(make_state){
            var self;
            self = this;
            if(!make_state){
                make_state = _make_state;
            };
            self._vm = new Vue({
                "data": make_state
            });
            self._state = self._vm.st;
            self.update = self._update.bind(self);
            self.set_prop = self._set_prop.bind(self);
            self.set = self._set.bind(self);
            self.get = self._get.bind(self);
        };
        get vm(){
            var self;
            self = this;
            return self._vm;
        };
        get state(){
            var self;
            self = this;
            return self._state;
        };
        get st(){
            var self;
            self = this;
            return self._state;
        };
        _update(patch){
            var self;
            self = this;
            self._patch_node(self.state, patch);
        };
        _patch_node(node, patch){
            var self, k, v;
            self = this;
            for(k of ϟ_iterable(patch)){
                v = patch[k];
                if(v._is_patch_){
                    self._patch_node(node[k], v.patch);
                }else{
                    self._set(node, k, v);
                };
            };
        };
        _set_prop(node, k, v){
            var self;
            self = this;
            self._vm.$set(node, k, v);
        };
        _set(){
            var self, path_v, vm, v, k, path, cur, p;
            self = this;
            path_v = [...arguments];
            vm = self._vm;
            v = path_v.pop();
            k = path_v.pop();
            path = path_v;
            cur = self._vm.st;
            for(p of ϟ_iterable(path)){
                if(cur[p] === undefined){
                    vm.$set(cur, p, {});
                };
                cur = cur[p];
            };
            vm.$set(cur, k, v);
        };
        _get(){
            var self, path, cur, p;
            self = this;
            path = [...arguments];
            cur = self._vm.st;
            for(p of ϟ_iterable(path)){
                cur = cur[p];
            };
            return cur;
        };
    };

    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:store"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["_make_state", ()=>_make_state, (v)=>{if (typeof _make_state !== "undefined") _make_state = v;}],
        ["AppStore", ()=>AppStore, (v)=>{if (typeof AppStore !== "undefined") AppStore = v;}]
    ]);
    return ϟ_mod;
};

 ϟ_modules["ϟ:store.AppStore"].ϟ_body = function (){
    var __name__ = "store.AppStore";
    function _make_state(){
        return {
            "st": JSON.parse(SPA_ENV.app_state)
        };
    };
    class AppStore{
        get __class__(){
            return this.constructor;
        };
        constructor(make_state){
            var self;
            self = this;
            if(!make_state){
                make_state = _make_state;
            };
            self._vm = new Vue({
                "data": make_state
            });
            self._state = self._vm.st;
            self.update = self._update.bind(self);
            self.set_prop = self._set_prop.bind(self);
            self.set = self._set.bind(self);
            self.get = self._get.bind(self);
        };
        get vm(){
            var self;
            self = this;
            return self._vm;
        };
        get state(){
            var self;
            self = this;
            return self._state;
        };
        get st(){
            var self;
            self = this;
            return self._state;
        };
        _update(patch){
            var self;
            self = this;
            self._patch_node(self.state, patch);
        };
        _patch_node(node, patch){
            var self, k, v;
            self = this;
            for(k of ϟ_iterable(patch)){
                v = patch[k];
                if(v._is_patch_){
                    self._patch_node(node[k], v.patch);
                }else{
                    self._set(node, k, v);
                };
            };
        };
        _set_prop(node, k, v){
            var self;
            self = this;
            self._vm.$set(node, k, v);
        };
        _set(){
            var self, path_v, vm, v, k, path, cur, p;
            self = this;
            path_v = [...arguments];
            vm = self._vm;
            v = path_v.pop();
            k = path_v.pop();
            path = path_v;
            cur = self._vm.st;
            for(p of ϟ_iterable(path)){
                if(cur[p] === undefined){
                    vm.$set(cur, p, {});
                };
                cur = cur[p];
            };
            vm.$set(cur, k, v);
        };
        _get(){
            var self, path, cur, p;
            self = this;
            path = [...arguments];
            cur = self._vm.st;
            for(p of ϟ_iterable(path)){
                cur = cur[p];
            };
            return cur;
        };
    };

    
    // exports
    var ϟ_mod = ϟ_modules["ϟ:store.AppStore"];
    ϟ_mod.export([
        ["__name__", ()=>__name__, null],
        ["_make_state", ()=>_make_state, (v)=>{if (typeof _make_state !== "undefined") _make_state = v;}],
        ["AppStore", ()=>AppStore, (v)=>{if (typeof AppStore !== "undefined") AppStore = v;}]
    ]);
    return ϟ_mod;
};
(function (){
    var __name__ = "__main__";
    function _init_(){
        var params, SPA_ENV;
        params = document.getElementsByTagName("meta")[0].dataset;
        SPA_ENV = window.SPA_ENV = Object.assign({}, params);
        SPA_ENV.app_static = SPA_ENV.app_base + "/static";
    };
    _init_();
    var app = ϟ_modules["app"];
    app.app.$mount("#app");
})()
})()