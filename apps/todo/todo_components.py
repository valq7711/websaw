from websaw import DefaultContext
from upytl import (
    Component, Slot, UPYTL, html as h
)

class TodoNavBar(Component):
    props = dict(
        buttons=[]
    )
    template = {
        h.Nav(Class='navbar is-dark', Role='navigation'): {
            h.Div(Class='navbar-brand'): {
                h.A(Class='navbar-item', href="https://bulma.io"): '',
            },
            h.Div(Id="navbarBasicExample", Class="navbar-menu"):{
                h.Div(Class='navbar-start'):{},
                h.Div(Class='navbar-end'): {
                    h.Div(Class='navbar-item'): {
                        h.Template(If = 'not buttons'):{
                            h.Div(): '',
                        },
                        h.Template(Else = ''):{
                            h.Div(Class='buttons'):{
                                h.Template(For='b in buttons'):{
                                    h.Template(If='b.get("vars", "")'):{
                                        h.A(Class={'b.get("class", "button")'},
                                            Href={'URL(b.get("href", "index"), vars=b.get("vars"))'}):'[[ b["name"] ]]',
                                    },
                                    h.Template(Else=''):{
                                        h.A(Class={'b.get("class", "button")'},
                                           Href={'URL(b.get("href", "index"))'}):'[[ b["name"] ]]',
                                    }
                                }
                            },
                        }
                    }
                }
            }
        }
    }

class TodoItem(Component):
    props = dict(
        item = None,
        update_ref = None,
        delete_ref = None,

    )
    template = {
        h.Link(rel="stylesheet", type="text/css", href="static/css/my.css"):None,

        h.Article(Class="media content-section"):{
            h.Div(Class="media-content"):{
                h.Div(Class='column has-text-right'):{
                    h.P(Class='content'):{
                        h.P():{
                            h.Small(Class="text-muted"): ' Last Action on [[item["date_added"].strftime("%B %d, %Y")]] ',
                            h.Small(): ' at [[item["date_added"].strftime("%H:%M")]]',
                        },
                    },
                },
                h.Div(Class='columns'):{
                    h.Div(Class='column is-8'):{
                        h.H2(Class="title is-size-4"):'[[ item["item"] ]]',
                    },
                    h.Div(Class='column buttons is-4 has-text-right'):{
                        h.A(If='update_ref',Class='button is-small is-success', href={'update_ref'}):'Update',
                        h.A(If='delete_ref', Class='button is-small is-danger' , href={'delete_ref'}): 'Delete',

                    }

                },
                h.Div(Class='column'):{
                    h.P(Class="article-content"):'[[ item["notes"] ]]',
                }


            }
        }
    }
    def get_context(self, rprops):
        ctx = DefaultContext.cctx()
        item = rprops['item']
        update_ref = None
        delete_ref = None

        update_ref = ctx.URL('todo', vars={'action':'update','pid': item['id']})
        delete_ref = ctx.URL('todo', vars={'action':'delete','pid': item['id']})

        return{**rprops,
                'update_ref':update_ref,
                'delete_ref':delete_ref,
              }



class TodoList(Component):
    props = dict(
        list = None,
    )
    template = {
        h.Div(Class='box'):{
            h.Div(For='item in list'):{
                TodoItem(
                    item = {'list[item]'},
                ):'',
            }
        }
    }
