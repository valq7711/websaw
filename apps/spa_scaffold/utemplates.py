from upytl import html as h, Component


meta_data = {
    'data-app_base': {'URL()'},
    'data-spa_name': '{spa_name}',
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
            h.Title(): 'spa-scaffold',
            h.Meta(charset='utf-8', **meta_data): None,
        },
        h.Body(): {
            h.Div(id="app"): None,  # here app will be mounted
            h.Script(src={'URL("static", "js/rs_require.js")'}): None,
            h.Script(src={"URL('static', f'spa_{spa_name}_routes.js')"}): None,
            h.Script(src={'URL("static", "js/index.js")'}): None,
        }
    }
}
