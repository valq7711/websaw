from websaw import DefaultContext, DefaultApp
import time


ctxd = DefaultContext()

app = DefaultApp(ctxd, name=__package__)

spa = app.spa()


@spa.main('index')
@app.use('index.html')
def index(ctx, **kw):
    return dict(spa_name=spa.name)


# spa-part of index-page
@spa.route('index')
@app.use('#index')  # no extension means it is bundled page (see vuepy/bandled_pages/)
def spa_index(ctx, **kw):
    return dict(index_data='index_data')


@spa.route('page-one', ['GET', 'POST'])
@spa.use('#page_one.js')
def page_one(ctx: DefaultContext):
    time.sleep(0.5)
    return {
        'msg': 'Hey from server',
        'count': 100
    }


@spa.route('page-two', ['GET', 'POST'])
@spa.use('#page_two.html')
def page_two(ctx: DefaultContext):
    return spa.response(data={}, alert='Hi! This is page-two')


@spa.route('page-three', ['GET', 'POST'])
@spa.use('#page_three.js')
def page_three(ctx: DefaultContext):
    return spa.response(data={}, alert='Hi')


@spa.route('search', ['GET', 'POST'])
@spa.use('#search.html')
def search(ctx: DefaultContext):
    data = dict(
        search_input=ctx.request.query.search,
        last_search_input=ctx.request.query.search,
        search_result=None,
    )
    if data['search_input']:
        if data['search_input'] == 'gold':
            data['search_result'] = ''
        else:
            data['search_result'] = f"You're searching for {data['search_input']}"
    return data


@spa.route('post-demo', ['GET', 'POST'])
@spa.use('#post_demo.html')
def search(ctx: DefaultContext):
    if ctx.request.method == 'POST':
        posted_msgs = ctx.request.json['posted_msgs'] or []
        posted_msgs.append(ctx.request.json['post_msg'])
        data = dict(
            posted_msgs=posted_msgs,
            post_msg='',
        )
    else:
        data = dict(
            posted_msgs = None,
            post_msg='',
        )
    return data

app.mount()