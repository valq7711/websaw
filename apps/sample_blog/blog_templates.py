from upytl import SlotTemplate, html as h
from upytl_standard import (
    HTMLPage,
    StandardForm,
    StandardNavBar
)
from .blog_components import (
    BlogIndex,
    BlogFlash,
    BlogNavBar,
)

# flake8: noqa E226

post_template={
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Jello'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            BlogFlash(flash={'form_options["flash"]'}):{},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class="columns"):{
                h.Div(Class="column is-8 is-offset-2"):{
                    h.Div(Class="card"):{
                        h.Div(Class="card-content"):{
                            h.P(Class="has-text-centered has-text-primary is-size-4"): 'My Blog Post',
                            h.Div():{
                                StandardForm(fields={'form_options["fields"]'}):{}, 
                            }
                        }
                    }
                }

            }
        }
    }
}

index_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Websaw Blog'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            BlogFlash(flash = {'form_options["flash"]'}):{},
        },
        
        SlotTemplate(Slot='content'):{
            BlogIndex(posts={'form_options["posts"]'}):{},
        }
    }
}    

