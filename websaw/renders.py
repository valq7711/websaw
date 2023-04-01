import json
from .core import BaseContext


def jsonfy(ctx: BaseContext, dct):
    ctx.response.headers['Content-Type'] = 'application/json'
    return json.dumps(dct, sort_keys=True, indent=2, ensure_ascii=False, default=str)


def spa_response(ctx: BaseContext, dct):
    ret = jsonfy(ctx, dct)
    ctx.response.headers['X-SPAResponse'] = True
    return ret
