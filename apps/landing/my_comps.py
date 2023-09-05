from upytl import (Component,Slot, html as h)

from upytl_standard import NavBarItem

class LandingPage(Component):
    props = dict(
        footer_class='page-footer',
        page_title="This is the page_title placeholder",
        nav = "This is our navbar placeholder"
    )
    template = {
        h.Html(): {
            h.Head():{
                h.Title(): '[[page_title]]',
                h.Meta(charset=b'utf-8'):'',
                },
            h.Body():{
                h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.4/css/bulma.min.css'):None, 
                h.Link(rel="stylesheet", href="https://cdn.datatables.net/1.10.24/css/jquery.dataTables.min.css"):None,
                h.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css", integrity="sha512-1PKOgIY59xJ8Co8+NE6FZ+LOAZKjy+KY8iq0G4B3CyeY6wYHN3yt9PW0XpSriVlkMXe40PTKnXrLnZ9+fkDaog==", crossorigin="anonymous"):None,
                h.Link(rel="stylesheet", href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css'):None,
                h.Link(rel="stylesheet", href={"URL('/landing/static', 'css/my.css')"}): None,
            
                h.Script(src="https://code.jquery.com/jquery-3.5.1.js"):None,
                h.Script(src="https://cdn.datatables.net/1.10.24/js/jquery.dataTables.min.js"):None,
                    
                Slot(SlotName=b'nav'):{
                    h.Div():'No NavBar passed to the form'
                },
                Slot(SlotName=b'flash'):{
                    h.Div():'No Flash Message passed to the form'
                },
                Slot(SlotName=b'content'):{h.Div(): '[there is no default content]'},
                Slot(SlotName=b'footer'):{
                    h.Footer(Class="footer is-small"):{
                        h.Div(Class= "content has-text-centered"):{
                            h.Template():{
                                h.P(): 'Powered by UPYTL Standard Components (c) 2023',
                            }    
                        }
                    }
                }
            }
        }
    }

class WebsawNavBar(Component):
    props = dict(
        menu = [],
        user = '',
        buttons=[]
    )
    template = {
        h.Nav(Class='navbar is-light is-fixed-top', Role='navigation'): {
            h.Div(Class='navbar-brand'): {
                h.A(Class='navbar-item my-navbar-item', href={'URL("index")'}):{
                    h.Figure(Class="image", height='100%'):{
                        h.Img(src={'URL("static/websaw.png")'} ):'',
                    }
                },
                h.A(
                    **{'aria-label':'menu', 'aria-expanded':"false"},
                    **{'data-target':"navbarStandard"},
                    role="button",
                    Class="navbar-burger is-active" 
                ):{
                    h.Span(**{'aria-hidden':'true'}):'',
                    h.Span(**{'aria-hidden':'true'}):'',
                    h.Span(**{'aria-hidden':'true'}):'',
                }

            },
            h.Div(Id="navbarStandard", Class="navbar-menu is-active"):{
                h.Div(Class='navbar-start'):{
                    h.Template(For='item in menu'):{
                        NavBarItem(
                            item = {'item'},
                        ):'',
                        
                    },
                    h.Div(Class='navbar-item has-text-info is-size-5 has-text-centered is-lowercase is-italic'):
                        'It is just the beginning ...',
                },
                h.Div(Class='navbar-end'): {
                    
                    h.Div(Class='buttons navbar-item'): {
                        h.Div(Class='navbar-item'): {
                            h.A(Class='button is-link is-light is-rounded has-text-link navbar-item'):{
                                h.Span(Class='icon'):{
                                    h.I(Class='fa fa-globe'):''
                                },
                                h.Span():'Websaw Home',
                            },
                            h.A(Class='button is-link is-light is-rounded has-text-link navbar-item'):{
                                h.Span(Class='icon'):{
                                    h.I(Class='fa fa-book'):''
                                },
                                h.Span():'Websaw User Guide',
                            },
                            h.A(Class='button is-link is-light is-rounded has-text-link navbar-item'):{
                                h.Span(Class='icon'):{
                                    h.I(Class='fa fa-code'):''
                                },
                                h.Span():'Websaw Awesome',
                            },
                            h.A(Class='button is-link is-light is-rounded has-text-link navbar-item'):{
                                h.Span(Class='icon'):{
                                    h.I(Class='fab fa-github'):''
                                },
                                h.Span():'Fork Me',
                            },
                            
                        }
                    }        
                    
                }
            },
            h.Script(): 
            '''
            $(document).ready(function() {
                // Check for click events on the navbar burger icon
                $(".navbar-burger").click(function() {

                    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                    $(".navbar-burger").toggleClass("is-active");
                    $(".navbar-menu").toggleClass("is-active");

                });
            });
            '''
        }
            
    }
    