from websaw import DefaultContext
from upytl import (
    Component, Slot, UPYTL, html as h
)
from upytl_standard import GridHeader, GridBody, RowButtons
import string


class Flash(Component):
    props = dict(
        flash = None,
        message = None,
        f_type=None
        )
    template = {
        h.Template():{
            h.Div(If='flash', Class='{f_type}'):{
                h.Span():'[[message]]',
            h.Button(Class='delete'): None,
            
            },
        },
        h.Script():
            """
            document.addEventListener('DOMContentLoaded', () => {
                (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
                    const $notification = $delete.parentNode;
                    $delete.addEventListener('click', () => {
                    $notification.parentNode.removeChild($notification);
                    });
                });
            });
            """
        
    }
    def get_context(self, rprops):
        ctx = DefaultContext.cctx()
        session = ctx.session
        flash = False
        f_message = session.get('flash_message', None)
        message = 'No Flash Message'
        flash_class = "notification has-text-centered is-info"
        if f_message:
            message = f_message.get('message', '')
            f_type = f_message.get('_class', None)
            
            if f_type:
                flash_class = "notification has-text-centered " + "is-" + f_type
                
            flash = True
            session['flash_message'] = ''
        return {**rprops, 'flash':flash, 'message':message, 'f_type':flash_class}

class DbAdminGrid(Component):
    props = dict(
        name = 'db_admin',
        columns = None,
        headers = None,
        data=None,
        fields = None,
        grid_buttons=None,
        )
    template = {
        h.Div(Class='box'):{
            h.Div(Class='columns'):{
                h.Div(Class='column is-8'):{
                    h.H4(Class='is-size-4'):'Database Administration',
                },    
                h.Div(Class='column is-4'):{
                    h.Div(For='button in grid_buttons', Class='button is-pulled-right'):'[[button]]',
                }    
            },
            h.Table(Id='db_admin', Class='table is-bordered is-striped'):{
                h.THead():{
                    h.TR():{
                        h.TH(For='header in headers'):'[[header]]',            
                    }
                }
            }        
        },
        h.Script(): '[[make_script(name, data, columns)]]'
              
    }    
    def get_context(self, rprops):
        return {**rprops, 'make_script': self.make_script}

    def make_script(self, name, data, columns):
        script = """$(document).ready( function () {
            $('#%s').DataTable({
                data: %s,
                columns: %s,
            })
        } );
        """ % (name, data, columns)
        return script

class DTCrud(Component):
    props = dict(
        title='',
        name = '',
        grid_buttons=[],
        name_stripped = '',
        columns = [],
        labels = [],
        data = [],
        
    )
    template = {
        h.Div(Class='box'):{
            h.Div(Class="column is-12 is-centered"):{
                h.Template():{
                    h.Span(Class='title is-4'): '[[title]]',
                    h.Span(For='button in grid_buttons',Class='is-pulled-right'):{
                        h.Div(Class='button is-small'):'[[button]]',
                    },
                },
            },
            h.Div(Class='column'):{
                h.Table(Id={'name_stripped'}, Class='table is-bordered is-striped nowrap', Style="width:100%"):{
                    h.THead():{
                        h.TR():{
                            GridHeader(columns={'columns'}, labels={'labels'}):{},
                        },
                    },
                    h.TBody():{
                        h.TR(For='dat in data'):{
                            GridBody(row={'dat'}, columns={'columns'}):{},
                        },
                    }
                },
                h.Script():"""$(document).ready( function () {
                $('#%s').DataTable({
                    scrollX : true,
                });    
                });""" % '[[ name_stripped ]]'
            }    
        },
        
    }
    def get_context(self, rprops):
        name = rprops['name']
        name_stripped = name.translate(str.maketrans('', '', string.whitespace))
        return{**rprops, 'name_stripped':name_stripped }
    

class HTMLCrud(Component):
    props = dict(
        title = '',
        name = '',
        grid_buttons='',
        columns = [],
        labels = [],
        data = []
    )
    template = {
        
        h.Div(Class='box'):{
            h.Div(Class="column is-12 is-centered"):{
                h.Template():{
                    h.Span(Class='title is-4'): '[[title]]',
                    h.Span(For='button in grid_buttons',Class='is-pulled-right'):{
                        h.Div(Class='button is-small'):'[[button]]',
                    },
                },
            },
            h.Table(id={'title'}, Class="table is-bordered is-striped", Style="width:100%"):{
                h.THead():{
                    h.TR():{
                        GridHeader(columns={'columns'}, labels={'labels'}):{},
                    },
                },
                h.TBody():{
                    h.TR(For='dat in data'):{
                        GridBody(row={'dat'}, columns={'columns'}):{},
                    },
                }
            }
        }
    }


class DTCRUD(Component):
    props = dict(
        title='',
        name = '',
        columns = [],
        data = []
    )
    template = {
        h.Div(Class='box'):{
            h.Table(Id={'name'}, Class="table is-bordered is-striped", Style="width:100%"):{
                h.THead():{
                    h.TR():{
                        h.TH(For='col in columns'): '[[ col.title() ]]',
                    },
                },
                h.TBody():{
                    h.TR(For='dat in data'):{
                        h.Template(For='d in dat'):{
                            h.TD(If='d in columns'): '[[ dat[d] ]]'    
                        },
                    },
                }
            },
            h.Script():"""$(document).ready( function () {
            $('#%s').DataTable()
            });""" % '[[ name ]]'
        }
    }
    
