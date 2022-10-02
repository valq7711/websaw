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
            Flash(): {},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class='box'):{
                h.Div(Class='title is-4'): 'Welcome [[user]] from the default_template_context',
                h.Div(Class='title is-5'): 'This is the basic app index Template. Select About to see more',
                h.Div(For='f in msg'):{
                    h.Text():'[[ f ]] : [[msg[f] ]]',
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
            Flash(): {},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class='section'):{
                h.Div(Class='box'):{
                    h.Div(Class='title is-5'): 'This is the mixin App about Template',
                    h.Div(Class='title is-5'): 'Click on the links below',
                    h.Div(For='f in msg'):{
                        h.A(Class='button is-medium is-fullwidth is-light is-link', href={'msg[f]'}):'[[ f ]] : [[msg[f] ]]',
                    }
                }
            }    
        }
    }
}
