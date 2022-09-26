from upytl import Slot, SlotTemplate, Component, html as h
from upytl_standard import HTMLPage, ViewOnlyForm, StandardForm 
from .grid_components import HTMLCrud, DTCrud

grid_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Todo'):{
        SlotTemplate(Slot='nav'):{},
        SlotTemplate(Slot='flash'):{},
        SlotTemplate(Slot='content'):{
            h.Template():{
                h.Div(Class="column"): 'This is the DT Crud grid',
                
                DTCrud(
                    title={'grid.get("title")'}, 
                    name={'grid.get("name", "No Name")'}, 
                    grid_buttons={'grid.get("grid_buttons")'},
                    columns={'grid.get("columns")'},
                    labels={'grid.get("labels")'}, 
                    data={'grid.get("data")'}
                ): {},
            },
            h.Template():{
                h.Div(Class="column"): 'This is the HTML Crud grid',
                HTMLCrud(
                    title={'grid.get("title")'}, 
                    name={'grid.get("name", "No Name")'}, 
                    grid_buttons={'grid.get("grid_buttons")'},
                    columns={'grid.get("columns")'},
                    labels={'grid.get("labels")'}, 
                    data={'grid.get("data")'}
                ): {},
            }
        }
    }
}        

action_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Todo'):{
        SlotTemplate(Slot='nav'):{},
        SlotTemplate(Slot='flash'):{},
        
        SlotTemplate(Slot='content'):{
            h.Template():{
                h.Section(If='show_button',Class='section'):{
                    StandardForm(fields={'form_options["fields"]'}):{},
                },
                h.Section(Else=''):{
                    ViewOnlyForm(fields={'form_options["fields"]'}):{},
                }
            }
        }
    }
}    

