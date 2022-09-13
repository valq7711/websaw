(function(){
"use strict";

(function(){

    var __name__ = "__main__";

    var params, SPA_ENV;
    params = document.getElementsByTagName("meta")[0].dataset;
    SPA_ENV = window.SPA_ENV = Object.assign({}, params);
    SPA_ENV.app_static = SPA_ENV.app_base + "/static";
    SPA_ENV.spa = {
        components: SPA_ENV.app_static + "spa/components",
        pages: SPA_ENV.app_static + "spa/pages"
    };
    define([ "amd" ], function(amd) {
        amd.config({
            base_url: SPA_ENV.app_static
        });
        amd.import("js/app").then(function(app) {
            app.$mount("#app");
        });
    });
})();
})();
