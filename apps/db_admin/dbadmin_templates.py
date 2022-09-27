from upytl import Slot, SlotTemplate, Component, html as h
from upytl_standard import HTMLPage, StandardNavBar, StandardForm, ViewOnlyForm
from .dbadmin_components import DTCrud, DbAdminGrid, Flash

dbadmin_template={
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'db_admin'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}):'',
        },
        SlotTemplate(Slot='flash'):{
            Flash():{}, #flash from auth mixin being used. This is just a placeholder
        },
        SlotTemplate(Slot='content'):{
            DbAdminGrid(headers={'grid_options["headers"]'}, 
                columns={'grid_options["columns"]'},
                data={'grid_options["data"]'},
                name={'grid_options["name"]'},
                grid_buttons={'grid_options.get("grid_buttons")'},
                
            ):{},
        }
    }
}

grid_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Table Admin'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}):'',
        },
        SlotTemplate(Slot='flash'):{
            Flash():{} #We are using flash from auth mixin
        },
        SlotTemplate(Slot='content'):{
            h.Link(rel="stylesheet", href="static/css/my.css"):None,
                
            h.Template():{
                
                DTCrud(
                    title={'grid.get("title")'}, 
                    name={'grid.get("name", "No Name")'}, 
                    grid_buttons={'grid.get("grid_buttons")'},
                    columns={'grid.get("columns")'},
                    labels={'grid.get("labels")'}, 
                    data={'grid.get("data")'}
                ): {},
            },
        }
    }
}        

action_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Todo'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}):'',
        },
        SlotTemplate(Slot='flash'):{
            Flash():{}, #and here as well
        },
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

