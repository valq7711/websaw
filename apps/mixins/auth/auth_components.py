from websaw import DefaultContext
from upytl import (Component,Slot, 
                    html as h
)
from upytl_standard import StandardField

from .upytl_form import BaseForm

class AuthFlash(Component):
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


class AuthPage(Component):
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


class ProfileForm(Component):
    props = dict(
        fields=None,
        flash = None,
        icon = None,
    )
    template = {
        h.Div(If='flash', Class="notification is-info has-text-centered"):'[[flash]]',
        h.Div(Class="media"):{
            h.Figure(Class="image media-left is-128x128"):{
                h.Img(Class='is-rounded', src={'icon'}, alt='No Image'):'' ,
            },
            h.Div(Class='media-content'):{
                h.P(Class='title is-4 is-primary'):'[[fields[1]["value"] ]] [[fields[2]["value"] ]]', #[[first_name]]',
                h.P(Class='subtitle'): '[[fields[3]["value"] ]]',
            },
        },    
        h.Form(If='fields', method='POST', Class='box', enctype='multipart/form-data'):{
            h.Template(For='fld in fields'):{
                h.Div(Class='field'):{
                    StandardField(field = {'fld'}):{},
                },
            },
            h.Div(Class='field'):{
                h.Input(Class='button is-success is-light', type='submit', value='Submit'): '',
                h.Input(Class='button is-danger is-light ', type='reset', value='Cancel'): '',
            }
        },
        h.Div(Else=''): 'Sorry, no fields were passed to this form'
    }
    def get_context(self, rprops):
        return{**rprops} 
