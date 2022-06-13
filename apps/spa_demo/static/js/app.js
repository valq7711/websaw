(function(){
"use strict";

(function(){

    var __name__ = "__main__";

    define([ "js/vue", "js/vue-router", "js/spa_tools", "js/spa_bundle" ], function(Vue, VueRouter, spa_tools, spa_bundle) {
        var app;
        spa_bundle.register_components(Vue);
        app = {
            router: spa_tools.make_router(SPA_ROUTES, spa_bundle.pages || {}),
            render: function(h) {
                return h("router-view");
            }
        };
        Vue.use(VueRouter);
        window.app = new Vue(app);
        return window.app;
    });
})();
})();
