from upytl import SlotTemplate, html as h 

from upytl_standard import HTMLPage, StandardNavBar 
from .auth_components import AuthFlash
# flake8: noqa E226

index = {
    HTMLPage(footer_class='custom-footer'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            AuthFlash(flash={'form_options["flash"]'}):{},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class='box'):{
                h.Div(Class='title is-4'): 'Welcome [[user]] from the default_template_context',
                h.Div(Class='title is-5'): 'This is the App Template',
                h.Div(For='f in msg'):{
                    h.Text():'[[ f ]] : [[msg[f] ]]',
                }
            }    
        }
    }
}

upytl_demo = {
    h.Html():{
        h.Head():{
            h.Title():"[[app_get('app_name')]]",
                h.Meta(charset='utf-8'):'',
                h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css'):None, 
            },
            h.Body():{
                h.Div(Class='box'):{
                    h.Div(Class='title'):'[[msg]]',
                }
            },    
            h.Footer():{
                h.Div(): 'This is the footer',
            }

        }
    }
