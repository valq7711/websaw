from upytl import html as h, Component, XTemplate, gtag


meta_data = {
    'data-app_base': {'URL()'},
}


class CSSLink(Component):
    def __init__(self, href: str):
        super().__init__(href=href)

    template = {
        h.Link(rel="stylesheet", type="text/css", href='{href}'): '',
    }


index = {
    h.Html(): {
        h.Head(): {
            h.Title(): 'vue-todo',
            h.Meta(charset='utf-8', **meta_data): None,
            h.Script(src="https://cdnjs.cloudflare.com/ajax/libs/axios/1.3.1/axios.js"): None,
            h.Script(src="https://cdn.jsdelivr.net/npm/vue@2/dist/vue.js"): None,
            h.Script(src={'URL("static", "js/upytl.js")'}): None,
            h.Script(src={'URL("static", "pyjs/index.js")'}): None,
        },
        h.Body(): {
            XTemplate(data={'todos_options'}): {
                gtag.Todo({':todos': 'todo_items', ':api': 'api_controller'}): ''
            }
        }
    }
}
