(function(){
"use strict";

(function(){

    var __name__ = "__main__";

    var templ, pg;
    templ = "\n<layout>\n    <p>This page stored in static/spa/pages/page_one.js</p>\n    <p>It was created using pyjsaw, src: vuepy/spa/pages/page_one.vuepy</p>\n    <p>After changes vuepy-file just press `Compile` to update js-file</p>\n    <button  @click = 'count+=1'>Click me</button>\n    <div>count: {{count}}</div>\n</layout>\n";
    pg = {
        template: templ,
        data: function data() {
            var self = this;
            return {
                count: 1
            };
        }
    };
    define([], function() {
        return pg;
    });
})();
})();
