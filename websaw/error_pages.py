
import http.client
import json

from upytl import UPYTL, html as h

from .core import globs

style = """
{
    color: white;
    text-align: center;
    background-color: [[ color ]];
    font-family: serif
}
h1{font-size:6em; margin: 16vh 0 8vh 0}
h2{font-size:2em; margin: 8vh 0}
a{
    color: white;
    text-decoration: none;
    font-weight: bold;
    padding: 10px 10px;
    border-radius: 10px;
    border: 2px solid #fff;
    transition: all .5s ease
}
a:hover{
    background: rgba(0,0,0,0.1);
    padding: 10px 30px
}
"""


default = {
    h.Html(): {
        h.Head(): {
            h.Style(): style,
        },
        h.Body(): {
            h.H1(): '[[ code ]]',
            h.H2(): '[[ message ]]',
            h.A(If='button_text', href='{href}'): '[[ button_text ]]'
        },
    }
}


ERROR_PAGES = {
    "*": default
}


def error_page(code, button_text=None, href="#", color=None, message=None):
    request = globs.request
    message = http.client.responses[code].upper() if message is None else message
    color = (
        {"4": "#F44336", "5": "#607D8B"}.get(str(code)[0], "#2196F3")
        if not color
        else color
    )
    context = dict(
        code=code, message=message, button_text=button_text, href=href, color=color
    )
    # if client accepts 'application/json' - return json
    if request.is_json_requested:
        globs.response.status = code
        return json.dumps(context)
    # else - return html error-page
    content = ERROR_PAGES.get(code) or ERROR_PAGES["*"]
    u = UPYTL()
    return u.render(content, context)
