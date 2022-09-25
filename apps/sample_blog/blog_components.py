from websaw import DefaultContext
from upytl import (
    Component, UPYTL, Slot, html as h
)

from . import settings
from upytl_standard import NavBarItem, StandardField

class BlogFlash(Component):
    props = dict(
        flash = None,
        message = None,
        f_type=None
        )
    template = {
        h.Template():{
            h.Div(If='flash', Class='{f_type}'):{
                h.Span():'[[message]]',
            h.Button(Class='delete'): None,
            
            },
        },
        h.Script():
            """
            document.addEventListener('DOMContentLoaded', () => {
                (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
                    const $notification = $delete.parentNode;
                    $delete.addEventListener('click', () => {
                    $notification.parentNode.removeChild($notification);
                    });
                });
            });
            """
        
    }
    def get_context(self, rprops):
        ctx = DefaultContext.cctx()
        session = ctx.session
        flash = False
        f_message = session.get('flash_message', None)
        message = 'No Flash Message'
        flash_class = "notification has-text-centered is-info"
        if f_message:
            message = f_message.get('message', '')
            f_type = f_message.get('_class', None)
            
            if f_type:
                flash_class = "notification has-text-centered " + "is-" + f_type
                
            flash = True
            session['flash_message'] = ''
        return {**rprops, 'flash':flash, 'message':message, 'f_type':flash_class}

class BlogNavBar(Component):
    props = dict(
        menu = [],
        user = '',
        buttons=[]
    )
    template = {
        h.Nav(Class='navbar is-light', Role='navigation'): {
            h.Div(Class='navbar-brand'): {
                h.A(Class='navbar-item', href="https://bulma.io"): '',   
            },
            h.Div(Id="navbarBasicExample", Class="navbar-menu"):{
                h.Div(Class='navbar-start'):{
                    h.Template(For='item in menu'):{
                        NavBarItem(
                            item = {'item'},
                        ):'',
                    },
                },
                h.Div(Class='navbar-end'): {
                    h.Div(Class='navbar-item'): {
                        h.Div(): 'Welcome [[ user ]]',
                    },
                    h.Div(Class='navbar-item'): {
                        h.Template(If = 'not buttons'):{
                            h.Div(): '',
                        },
                        h.Template(Else = ''):{
                            h.Div(Class='buttons'):{
                                h.A(For = 'b in buttons',Class={'b.get("class", "button")'}, Href={'b.get("href", "index")'}):'[[ b["name"] ]]',
                            },
                        }        
                    }
                }
            }
        }    
    }
    def get_context(self, rprops):
        ctx = DefaultContext.cctx()
        buttons = rprops['buttons']
        for i, j in enumerate(buttons):
            print('button', buttons[i])
            ref = buttons[i].get('href')
            buttons[i]['href'] = str(ctx.URL(ref))
            
        print('buttons', buttons)
        return{**rprops}

class BlogPage(Component):
    props = dict(
        footer_class='page-footer',
        page_title="Page title will be set when we initialise the component",
        nav = "This will be our navbar"
    )
    template = {
        h.Html(): {
            h.Head():{
                h.Title(): '[[page_title]]',
                h.Meta(charset=b'utf-8'):'',
                },
            h.Body():{
                
                h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css'):None, 
                h.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css", integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==", crossorigin="anonymous"):None,
                
                h.Script(src="https://code.jquery.com/jquery-3.5.1.js"):None,    
                
                Slot(SlotName=b'nav'):{
                    h.Div():'No Navbar for this form' 
                },    
                Slot(SlotName=b'flash'):{
                    h.Div(): 'No Flash Component for this form'
                },
                Slot(SlotName=b'content'):{h.Div(): '[there is no default content]'},
                Slot(SlotName=b'footer'):{
                    
                    h.Footer(Class="footer is-small"):{
                        h.Div(Class= "content has-text-centered"):{
                            h.Template():{
                                h.P(): 'Powered by <img src="static/mxn/auth/websaw_logo.png" width="100">'+ "  "+'and UPYTL-Standard components (c) 2022'
                            }    
                        }
                    }
                }
            }
        }
    }

class BlogPost(Component):
    props = dict(
        post = None,
        profile_image = None,
        user_ref = None,
        view_ref = None,
        update_ref = None,
        delete_ref = None
    )
    template = {
        h.Link(rel="stylesheet", type="text/css", href="static/css/my.css"):None,
                
        h.Article(Class="media content-section"):{
            h.Figure(Class="media-left"):{
                h.P(Class="image article-img"):{
                    h.Img(Class="image is-rounded",src={'profile_image'}):{
                    }
                }
            },
            h.Div(Class="media-content"):{
                h.P(Class='content'):{
                    h.P():{
                        h.A(Class='is-size-4', href={'user_ref'}): '[[post.post.author.username]] ',
                        h.Small(Class="text-muted"): ' [[post.post.date_posted.strftime("%B %d, %Y")]] ',
                        h.Small(): ' at [[post.post.date_posted.strftime("%H:%M")]]',    
                    },
                    h.Div():{
                        h.A(If='update_ref',Class='button is-small is-light is-success', href={'update_ref'}):'Update',
                        h.A(If='delete_ref', Class='button is-small is-light is-danger' , href={'delete_ref'}): 'Delete',
                
                    },
                    
                },
                h.A(Class="article-title", href={'user_ref'}):{
                    h.H2(Class="title is-size-3"):'[[post.post.title]]',
                },
                h.P(Class="article-content"):'[[post.post.content]]',
                        
            }
        }
    }
    def get_context(self, rprops):
        ctx = DefaultContext.cctx()
        post = rprops['post']
        user = ctx.auth.user
        update_ref = None
        delete_ref = None
        
        if user and user['id'] == post.post.author.id:
            update_ref = ctx.URL('post', vars={'action':'update','pid': post.post.id})
            delete_ref = ctx.URL('post', vars={'action':'delete','pid': post.post.id})
        p_image = ctx.URL('static/images/',post.profile.image)#+ post.profile.image
        u_href = ctx.URL('index', vars={'filter_by':'user','uid': post.post.author.id})
        
        return{**rprops, 'profile_image':p_image,
                'update_ref':update_ref,
                'delete_ref':delete_ref,
                'user_ref':u_href
              } 

class BlogIndex(Component):
    props = dict(
        posts = None,
        flash = None
    )
    template = {
        h.Div(If='flash', Class="notification is-info has-text-centered"):'[[flash]]',
        
        h.Div(Class='container'):{
            h.Template(For='post in posts'):{
                h.Div(Class="box"):{
                    BlogPost(
                    post = {'post'},
                    ):'',
                }
            }
        }
    }    

