from upytl import html as h, Component


meta_data = {
    'data-app_base': {'URL()'},
    'data-spa_name': '{spa_name}',
    'data-app_state': '{app_state}',
}


class CSSLink(Component):
    props = {
        'href': ''
    }

    template = {
        h.Link(rel="stylesheet", type="text/css", href='{href}'): '',
    }


index = {
    h.Html(): {
        h.Head(): {
            h.Title(): 'Spa Todo MVC',
            h.Meta(charset='utf-8', **meta_data): None,
            h.Link(rel = "shortcut icon", type = "image/x-icon", href = {"URL('static', 'favicon.ico')"}):None,
        },
        h.Body(): {
            h.Div(id="app"): None,  # here the app will be mounted
            
            h.Link(rel="stylesheet", href={"URL('static', 'css/todo.css')"}): None,
            
            h.Script(src={"URL('static', f'spa_{spa_name}_routes.js')"}): None,
            h.Script(src={'URL("static", "js/axios.min.js")'}): None,
            h.Script(src={'URL("static", "js/vue.js")'}): None,
            h.Script(src={'URL("static", "js/vue-router.js")'}): None,
            h.Script(src={'URL("static", "pyjs/index.js")'}): None,
        }
    }
}
