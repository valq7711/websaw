from upytl import SlotTemplate, html as h
from upytl_standard import HTMLPage, StandardForm, StandardNavBar, HTMLGrid
from .todo_components import TodoList, TodoNavBar

todo_template = {
    HTMLPage(footer_class='custom-footer', nav='No nave here', page_title = 'Todo'):{
        SlotTemplate(Slot='nav'):{
            TodoNavBar(buttons=[
                {'name':'New Todo', 'href':'todo', 'vars':{'action':'new'}},
                {'name': 'Todo List', 'href':'index'},
            ]):{}
        },
        SlotTemplate(Slot='flash'): {},
        
        SlotTemplate(Slot='content'):{
            h.Template():{
                
                h.Section(Class='section'):{
                    h.Div(Class='contianer'):{
                        h.Div(Class='columns'):{
                            h.Div(Class='column is-half'):{
                                h.Div(Class='notification is-primary'): 'You have been here [[ session["counter"] ]] times',
                            },
                            h.Div(Class='column is-half'):{
                                h.Div(Class='notification is-primary'): 'You currently have [[items_count]] items in your TODO list ',
                            }
                        },
                        
                        h.Template(If='show_form'):{
                            StandardForm(fields={'form_options["fields"]'}):{},
                        },    
                        h.Template(Else=''):{
                            h.Div(Class='column'):{
                                TodoList(list={'items'}):{},
                            }    
                        }
                    }            
                }        
            }
        }
    }
}    
