from pyjsaw.typing.jstyping import window, Object


def _init_():
    params = document.getElementsByTagName('meta')[0].dataset
    WEBSAW_ENV = window.WEBSAW_ENV = Object.assign({}, params)
    WEBSAW_ENV.app_static = WEBSAW_ENV.app_base + '/static'
    import main

_init_()

