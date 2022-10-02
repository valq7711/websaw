from upytl import Slot, SlotTemplate, Component, html as h
from upytl_standard import HTMLPage, DTGrid, HTMLGrid 

grid_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Todo'):{
        SlotTemplate(Slot='nav'):{},
        SlotTemplate(Slot='flash'):{},
        SlotTemplate(Slot='content'):{
            h.Template():{
                h.Div(Class="column"): 'This is a simple DT grid',
                
                DTGrid(
                    title={'grid.get("title")'}, 
                    name={'grid.get("name", "No Name")'}, 
                    grid_buttons={'grid.get("grid_buttons")'},
                    columns={'grid.get("columns")'},
                    labels={'grid.get("labels")'}, 
                    data={'grid.get("data")'}
                ): {},
            },
            h.Template():{
                h.Div(Class="column"): 'This is a simple HTML grid',
                HTMLGrid(
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
