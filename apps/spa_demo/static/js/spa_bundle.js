(function(){
"use strict";
var ՐՏ_1, ՐՏ_2;
function ՐՏ_extends(child, parent) {
    child.prototype = Object.create(parent.prototype);
    child.prototype.__base__ = parent;
    child.prototype.constructor = child;
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
class KeyError extends Error {
    constructor (message) {
        super();
        var self = this;
        self.name = "KeyError";
        self.message = message;
    }
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
ՐՏ_modules.ՐՏ_def("asset.mechanic");
ՐՏ_modules.ՐՏ_def("asset");
ՐՏ_modules.ՐՏ_def("spa_tools");
ՐՏ_modules.ՐՏ_def("bundled_pages.index");
ՐՏ_modules.ՐՏ_def("bundled_pages");
ՐՏ_modules.ՐՏ_def("bundled_components.layout");
ՐՏ_modules.ՐՏ_def("bundled_components");

ՐՏ_modules["ՐՏ:asset.mechanic"].body = function(){
    var __name__ = "asset.mechanic";

    var RS_MODULES;
    RS_MODULES = ՐՏ_modules;
    function module(mod_id) {
        if (mod_id) {
            return RS_MODULES[mod_id];
        }
        function all_() {
            var ret;
            ret = {};
            for (var k in RS_MODULES) {
                if (!k.startsWith("ՐՏ:")) {
                    ret[k] = RS_MODULES[k];
                }
            }
            return ret;
        }
        function keys() {
            var ret;
            ret = [];
            for (var k in RS_MODULES) {
                if (!k.startsWith("ՐՏ:")) {
                    ret.push(k);
                }
            }
            return ret;
        }
        return {
            "all": all_,
            keys: keys
        };
    }
    function module_spec(mod_id) {
        if (mod_id) {
            return RS_MODULES["ՐՏ:" + mod_id];
        }
        return {
            "all": function() {
                var ret;
                ret = {};
                module().keys().forEach(function(k) {
                    ret[k] = module_spec(k);
                });
                return ret;
            },
            "undefined": function() {
                var ret;
                ret = {};
                module().keys().forEach(function(k) {
                    var ms;
                    ms = module_spec(k);
                    if (!(ms.exports || ms.body)) {
                        ret[k] = ms;
                    }
                });
                return ret;
            },
            "defined": function() {
                var ret;
                ret = {};
                module().keys().forEach(function(k) {
                    var ms;
                    ms = module_spec(k);
                    if (ms.exports || ms.body) {
                        ret[k] = ms;
                    }
                });
                return ret;
            }
        };
    }
    function create_module(mod_name, pack_id) {
        var mod_id, pack, rs_mod_id;
        mod_id = pack_id ? pack_id + "." + mod_name : mod_name;
        if (module_spec(mod_id)) {
            throw new KeyError("Module exists: " + mod_id);
        }
        if (pack_id) {
            pack = module_spec(pack_id);
            if (!pack) {
                throw new KeyError("Package doesn't exists: " + pack_id);
            }
        } else {
            pack = null;
        }
        RS_MODULES.ՐՏ_def_mod(mod_id);
        if (pack) {
            rs_mod_id = "ՐՏ:" + mod_id;
            pack.export(mod_name, function() {
                return RS_MODULES[rs_mod_id].exports;
            }, function(v) {
                replace_module(mod_id, v);
            });
        }
    }
    function replace_module(mod_id, new_exp) {
        var ՐՏitr1, ՐՏidx1;
        var mod_spec, exp, p;
        if (!(mod_spec = module_spec(mod_id))) {
            throw new KeyError("Module doesn't exist: " + mod_id);
        }
        ՐՏitr1 = ՐՏ_Iterable(exp = mod_spec.exports);
        for (ՐՏidx1 = 0; ՐՏidx1 < ՐՏitr1.length; ՐՏidx1++) {
            p = ՐՏitr1[ՐՏidx1];
            delete exp[p];
        }
        Object.defineProperties(exp, Object.getOwnPropertyDescriptors(new_exp));
    }
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset.mechanic"];
    ՐՏ_mod.export("RS_MODULES", function(){return RS_MODULES;}, function(ՐՏ_v){if (typeof RS_MODULES !== "undefined") {RS_MODULES = ՐՏ_v;};});
    ՐՏ_mod.export("module", function(){return module;}, function(ՐՏ_v){if (typeof module !== "undefined") {module = ՐՏ_v;};});
    ՐՏ_mod.export("module_spec", function(){return module_spec;}, function(ՐՏ_v){if (typeof module_spec !== "undefined") {module_spec = ՐՏ_v;};});
    ՐՏ_mod.export("create_module", function(){return create_module;}, function(ՐՏ_v){if (typeof create_module !== "undefined") {create_module = ՐՏ_v;};});
    ՐՏ_mod.export("replace_module", function(){return replace_module;}, function(ՐՏ_v){if (typeof replace_module !== "undefined") {replace_module = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:asset"].body = function(){
    var __name__ = "asset";

    ՐՏ_modules["ՐՏ:asset"].export("mechanic", function(){return ՐՏ_modules["asset.mechanic"];}, function(){throw new Error("use Object.defineProperty!");});

    var ՐՏ_mod = ՐՏ_modules["ՐՏ:asset"];
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:bundled_pages.index"].body = function(){
    var __name__ = "bundled_pages.index";

    var templ, vc;
    templ = "\n<layout>\n    <p>This is spa-part of Index-page</p>\n    <p>It was created using pyjsaw, src: vuepy/bundled_pages/index.vuepy</p>\n    <p>It is bundled into spa_bundle.pyj which is compiled to static/js/spa_bundle.js</p>\n</layout>\n";
    var spa_tools = ՐՏ_modules["spa_tools"];
    vc = spa_tools.v_collector();
    
    var Page = (ՐՏ_1 = class Page extends spa_tools.RSVue {
        constructor () {
            super();
            var self = this;
            self.name = __name__;
            self.template = templ;
        }
    }, ՐՏ_1 = vc.component()(ՐՏ_1), ՐՏ_1);
    function make() {
        return new Page();
    }
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:bundled_pages.index"];
    ՐՏ_mod.export("templ", function(){return templ;}, function(ՐՏ_v){if (typeof templ !== "undefined") {templ = ՐՏ_v;};});
    ՐՏ_mod.export("vc", function(){return vc;}, function(ՐՏ_v){if (typeof vc !== "undefined") {vc = ՐՏ_v;};});
    ՐՏ_mod.export("Page", function(){return Page;}, function(ՐՏ_v){if (typeof Page !== "undefined") {Page = ՐՏ_v;};});
    ՐՏ_mod.export("make", function(){return make;}, function(ՐՏ_v){if (typeof make !== "undefined") {make = ՐՏ_v;};});
    ՐՏ_mod.export("spa_tools", function(){return spa_tools;}, function(ՐՏ_v){if (typeof spa_tools !== "undefined") {spa_tools = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:bundled_pages"].body = function(){
    var __name__ = "bundled_pages";

    ՐՏ_modules["ՐՏ:bundled_pages"].export("index", function(){return ՐՏ_modules["bundled_pages.index"];}, function(){throw new Error("use Object.defineProperty!");});
    var index = ՐՏ_modules["bundled_pages.index"];
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:bundled_pages"];
    ՐՏ_mod.export("index", function(){return index;}, function(ՐՏ_v){if (typeof index !== "undefined") {index = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:bundled_components.layout"].body = function(){
    var __name__ = "bundled_components.layout";

    var templ, vc;
    templ = "\n<div>\n    <h2>This is layout (vuepy/bundled_components/layout.vuepy)</h2>\n    <nav>\n        <router-link  to = \"/page-one\">One</router-link>\n        <router-link  to = '/page-two'>Two</router-link>\n        <router-link  to = '/page-three'>Three</router-link>\n        <router-link  to = '/search'>Search</router-link>\n        <router-link  to = '/post-demo'>Post demo</router-link>\n    </nav>\n    <h1>Current URI: {{$route.fullPath}}</h1>\n    <p>Page Content:</p>\n    <div  style = 'padding-left: 50px; background-color: #eee;'>\n        <slot></slot>\n    </div>\n    <div>\n        <router-link  to = '/index'>index</router-link>\n    </div>\n</div>\n";
    var spa_tools = ՐՏ_modules["spa_tools"];
    vc = spa_tools.v_collector();
    
    var Component = (ՐՏ_2 = class Component extends spa_tools.RSVue {
        constructor () {
            super();
            var self = this;
            self.name = __name__;
            self.template = templ;
        }
    }, ՐՏ_2 = vc.component()(ՐՏ_2), ՐՏ_2);
    function make() {
        return new Component();
    }
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:bundled_components.layout"];
    ՐՏ_mod.export("templ", function(){return templ;}, function(ՐՏ_v){if (typeof templ !== "undefined") {templ = ՐՏ_v;};});
    ՐՏ_mod.export("vc", function(){return vc;}, function(ՐՏ_v){if (typeof vc !== "undefined") {vc = ՐՏ_v;};});
    ՐՏ_mod.export("Component", function(){return Component;}, function(ՐՏ_v){if (typeof Component !== "undefined") {Component = ՐՏ_v;};});
    ՐՏ_mod.export("make", function(){return make;}, function(ՐՏ_v){if (typeof make !== "undefined") {make = ՐՏ_v;};});
    ՐՏ_mod.export("spa_tools", function(){return spa_tools;}, function(ՐՏ_v){if (typeof spa_tools !== "undefined") {spa_tools = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

ՐՏ_modules["ՐՏ:bundled_components"].body = function(){
    var __name__ = "bundled_components";

    ՐՏ_modules["ՐՏ:bundled_components"].export("layout", function(){return ՐՏ_modules["bundled_components.layout"];}, function(){throw new Error("use Object.defineProperty!");});
    var layout = ՐՏ_modules["bundled_components.layout"];
    var ՐՏ_mod = ՐՏ_modules["ՐՏ:bundled_components"];
    ՐՏ_mod.export("layout", function(){return layout;}, function(ՐՏ_v){if (typeof layout !== "undefined") {layout = ՐՏ_v;};});
    return ՐՏ_mod["exports"];
};

(function(){

    var __name__ = "__main__";

    function make(spa_tools) {
        var mechanic = ՐՏ_modules["asset.mechanic"];
        mechanic.module_spec("spa_tools").exports = spa_tools;
        var spa_pages = ՐՏ_modules["bundled_pages"];
        var spa_components = ՐՏ_modules["bundled_components"];
        function register_components(Vue) {
            var ՐՏitr2, ՐՏidx2, ՐՏ_3;
            var module_name, c, cid;
            if (!spa_components) {
                return;
            }
            ՐՏitr2 = ՐՏ_Iterable(spa_components);
            for (ՐՏidx2 = 0; ՐՏidx2 < ՐՏitr2.length; ՐՏidx2++) {
                module_name = ՐՏitr2[ՐՏidx2];
                c = spa_components[module_name].make();
                cid = (ՐՏ_3 = c.name.split("."))[ՐՏ_3.length-1];
                Vue.component(cid, c);
            }
        }
        return {
            pages: spa_pages,
            components: spa_components,
            register_components: register_components
        };
    }
    define([ "js/spa_tools" ], function(spa_tools) {
        return make(spa_tools);
    });
})();
})();
