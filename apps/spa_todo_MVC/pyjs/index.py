def _init_():
    params = document.getElementsByTagName('meta')[0].dataset
    SPA_ENV = window.SPA_ENV = Object.assign({}, params)
    SPA_ENV.app_static = SPA_ENV.app_base + '/static'

_init_()


import app


app.app.S_mount('#app')
