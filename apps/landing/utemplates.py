from upytl import SlotTemplate, html as h 

from upytl_standard import HTMLPage
from . my_comps import LandingPage, WebsawNavBar
 
from ..common.common_components import Flash
# flake8: noqa E226

index = {
    LandingPage(footer_class='custom-footer'):{
        SlotTemplate(Slot='nav'):{
            WebsawNavBar(menu={'menu'}, buttons={'buttons'}): '',        
                
        },
        SlotTemplate(Slot='flash'):{
            Flash(flash=()):{}
        },
        
        SlotTemplate(Slot='content'):{
            
            h.Section(Class='section'):{
                h.Div(Class='box has-bg-img'):{
                    h.Div(Class = 'column is-12 subtitle'): 
                        'The following applications are shipped with Websaw as standard in order to demonstrate some of the rich \
                        fucntionlatiy and flexibility that comes as standard with Websaw. In order to fully understand \
                        the full scope or if you are new to Websaw, we stongly reccomend a tour of the comprehensive \
                        Websaw User Guide where the priciples demonstrated are explained in much greater depth.',
                        
                    h.Div(Class='columns'):{
                        h.Div(Class='column is-6'):{
                            h.Div(Class='subtitle is-4 has-text-weight-semibold has-text-grey-light'):'Serverside Apps',
                                
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth',href='/grid'):'grid',
                                },
                                h.Div(Class='column is-9'): 
                                    'Applciation demonstrating the use of both standard HTML as well as Datatables GRID components from the UPYTL-Standard components library',
                            },    
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='/group_session/login'):'group_session',
                                },
                                h.Div(Class='column is-9'):
                                    'A Bare bones application demonstrating group session integration to your application'
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth'):'landing',
                                },
                                h.Div(Class='column is-9'): 'This Application',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='/sample_blog/'):'sample_blog',
                                },
                                h.Div(Class='column is-9'):
                                    'A sample blog app built using upytl standard components demonstrating multiple \
                                    aspects of websaw including the use of MIXINS and database access',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='/sample_crud'):'sample_crud',
                                },
                                h.Div(Class='column is-9'):
                                    'As with the sample_grid this app demonstrates the integration of two types of CRUD \
                                    components from UPYTL-standard that ships with Websaw',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='/scaffold'):'scaffold',
                                },
                                h.Div(Class='column is-9'): 
                                    'This is generally the starting point for any new app and as the name suggests\
                                    offers a fully functional application from which to start your new application',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='skeleton'):'skeleton',
                                },
                                h.Div(Class='column is-9'): 
                                    'For those who wish to start a project from "bare bones", this app is the one for you.',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='/todo'):'todo',
                                },
                                h.Div(Class='column is-9'): 
                                    'The one App that no self respecting framework should be without',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth', href='/xauth/login'):'xauth',
                                },
                                h.Div(Class='column is-9'): 
                                    'Demonstates the base integration of the Auth fixture in your App',
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-link is-fullwidth'):'xtemplate',
                                },
                                h.Div(Class='column is-9'): 
                                    'Demonstrates interchanging templates between host app and MIXIN in both directions',
                            }
                        },
                        h.Div(Class='column is-6'):{
                            h.Div(Class='subtitle is-4 has-text-weight-semibold has-text-grey-light'):'SPA Apps',
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-9'): 
                                    'This app demonsrates how to develop a SPA by porting the Vue spa_MVC \
                                    app (as per the official Vue 2 documentaion) in order to highlight the differences',
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-primary is-fullwidth', href='/spa_todo_MVC'):'spa_todo_MVC',
                                }
                            },
                            h.Div(Class='subtitle is-4 has-text-weight-semibold has-text-grey-light'):'Mixins',
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-9'): 
                                    'The Auth mixin provides "out of the box" role based authorisation and authentication for \
                                    user access to your applications. Functionality includes user registration, profile updates \
                                    roles, memberships authentification and much more', 
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-info is-light is-fullwidth'):'mixins/auth',
                                }
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-9'): 
                                    'The Database Administration mixin give you CRUD access to all databases and tables used \
                                    in any applciation that emploay this mixin. Typically used in conjuction with the Auth mixin in order \
                                    to ensure that only the users with appropriate access rights can access all data.',
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-info is-light is-fullwidth'):'mixins/db_admin',
                                }
                            },
                            h.Div(Class='columns'):{
                                h.Div(Class='column is-9'): 
                                    'The Info mixin is a usefull utility mixin which displays a wealth of low level information about the applicaiton \
                                    it is included in. In addition it demonstrates some key Websaw features usefull in all applications.',
                                h.Div(Class='column is-3'):{
                                    h.A(Class='button is-info is-light is-fullwidth'):'mixins/info',
                                }
                            }
                        }    
                    }
                }
            }
        }
    }
}

about = {
    HTMLPage(footer_class='custom-footer'):{
        SlotTemplate(Slot='nav'):{
            WebsawNavBar(menu={'menu'}, user= {'user'}, buttons={'buttons'}): '',
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

