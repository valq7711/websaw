from websaw import DefaultContext
from upytl import (
    Component, Slot, UPYTL, html as h
)
from upytl_standard import GridHeader, GridBody, RowButtons
import string

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
            h.Table(Id={'name_stripped'}, Class="table is-bordered is-striped", Style="width:100%"):{
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
            $('#%s').DataTable()
            });""" % '[[ name_stripped ]]'
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
