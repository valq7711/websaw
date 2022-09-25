from upytl import SlotTemplate, html as h 
from upytl_standard import StandardNavBar, StandardForm
from .auth_components import (AuthPage, AuthFlash, ProfileForm)

profile_template = {
    AuthPage(page_title='Profile', footer_class='custom-footer'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            AuthFlash(flash={'form_options["flash"]'}):{},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class="columns"):{
                h.Div(Class="column is-6 is-offset-one-quarter"):{
                    h.Div(Class="card"):{
                        h.Div(Class="card-content"):{
                            SlotTemplate(slot='profile'):{
                                ProfileForm(fields={'form_options["fields"]'},
                                            icon={'icon'},
                                ):{},
                            },
                        }
                    }
                }
            }                    
        }
    }
}

login_template = {
    AuthPage(footer_class='custom-footer', page_title = 'Login'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu='', user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            AuthFlash(flash={'form_options["flash"]'}):{},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class="section is-medium"):{
                h.Div(Class="columns is-centered"):{
                    h.Div(Class="box colum is-5-tablet is-4-desktop is-3-widescreen"):{
                        h.Div(Class='is-size-5 has-text-centered has-text-primary'):"Please Login",
                        StandardForm(fields={'form_options["fields"]'}):{}, 
                    }
                }
            } 
        }
    }
}

register_template={
    AuthPage(footer_class='custom-footer', nav='No nave here', page_title = 'Register'):{
        SlotTemplate(Slot='nav'):{
            StandardNavBar(menu='', user= {'user'}, buttons={'buttons'}): '',
        },
        SlotTemplate(Slot='flash'):{
            AuthFlash(flash={'form_options["flash"]'}):{},
        },
        SlotTemplate(Slot='content'):{
            h.Div(Class="columns"):{
                h.Div(Class="column is-6 is-offset-one-quarter"):{
                    h.Div(Class="card"):{
                        h.Div(Class="card-content"):{
                            h.P(Class="has-text-centered has-text-primary is-size-4"): 'Register',
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
