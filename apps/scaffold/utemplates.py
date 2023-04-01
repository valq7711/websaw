from upytl import SlotTemplate, html as h 

from upytl_standard import HTMLPage, StandardNavBar 
from ..common.common_components import Flash
# flake8: noqa E226

index = {
    HTMLPage(footer_class='custom-footer'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            Flash(flash=()):{}
        },
        
        SlotTemplate(Slot='content'):{
            h.Div(Class='section'):{
                h.Div(Class='box'):{
                    h.Div(Class='title is-4'): 'Welcome [[user]] to the scaffold app',
                    h.Div(Class='title is-5'): 'This is your quick start for creating beautifull apps',
                    h.Div(Class='title has-text-centered is-default'):'[[ msg ]]',
                }
            }
        }
    }
}

about = {
    HTMLPage(footer_class='custom-footer'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            Flash(flash=()):{}
        },
        
        SlotTemplate(Slot='content'):{
            h.Div(Class='section'):{
                h.Div(Class='box'):{
                    h.Div(Class='title is-5'): 'This is all the information related to the scaffold app. You can format all in the about template',
                    h.Div(For='f in msg'):{
                        h.Text():'[[ f ]] : [[msg[f] ]]',
                    }
                }
            }    
        }
        
    }
}

