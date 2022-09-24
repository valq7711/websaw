import os

"""
This is the Base Class from which all grids should be built. Any overrides should be done
in specific classes
"""

class BaseGrid:
    """
    Usage in websaw controller:

       def index():
           grid = Grid(db.thing, record=1)
           return dict(grid=grid)

    Arguments:
    - db name we are using as defined in DBRegistry must be a string
    - table: a DAL table or a list of fields
    - fields: a list of fields to display
    - create: set to False to disable creation of new record
    - editable: set to False to disallow editing of record seletion
    - deletable: set to False to disallow deleting of record seletion
    - links: list of addtional links to other tables
    - form_name: the optional name for this grid
    - serverside: set to False for client side processing
    """

    def __init__(self, 
                ctx = None,
                cdb = None,
                table = None,
                **kwargs):
        
        allowed_args = ('create', 'editable', 'deletable', 'viewable',
                        'upload', 'download', 'b_button', 'links', 'page_title',
                        'show_id', 'hide', 'order','grid_type', 'serverside')
        
        default_values = dict(create=True, editable=True, deletable=True, viewable=True, links=None,
                              upload=False, download=False, b_button = None,  page_title=None,
                              show_id=True, hide=[], grid_type='HTMLGrid', order=['0', 'asc'],
                              serverside=False)
                 
        self.__dict__.update(default_values)
        if set(kwargs.keys()).issubset(allowed_args):
            self.__dict__.update(kwargs)
        else:
            disallowed_args = set(kwargs.keys()).difference(allowed_args)
            raise Exception (f'The following unsupported argument(s) was passed to BaseGrid:\n{disallowed_args}')
        
        #  positional args
        self.ctx = ctx
        self.cdb = cdb
        self.table = table
        
        #  all the rest
        self.frm_buttons = None
        self.headers = None
        self.fields = None
        self.accepted = True
        
        self.db = ctx.ask(self.cdb)

    def get_options(self):
        # not implemented
        ...

    @staticmethod
    def grid_button(
            button_type,
            title = '',
            href=''
        ):
        title = ''
        icon = ''
        
        if button_type == 'table':
            title = title or 'Table'
            icon = 'fas fa-list text-info'

        elif button_type == 'view':
            title = title or 'View'
            icon = 'fas fa-search-location text-info'
            
        elif button_type == 'create':
            title=title or 'Create'
            icon = 'fa fa-plus '
            
        elif button_type == 'update':
            title = title or 'Update'
            icon = 'fas fa-cog'
            
        elif button_type == 'delete':
            title = title or 'Delete'
            icon = 'fa fa-trash'
            
        elif button_type == 'upload_csv':
            title = title or "Upload CSV"
            icon = "fas fa-upload"
        
        elif button_type == 'download':
            title = title or "Download"
            icon = 'fas fa-download'

        else:
            title='Unknown button type'
            icon = ''
            href="#"

        button = '<a href="%s"><i class="%s"></i>&nbsp;%s</a>' %(href, icon, title)
        return button

    
    def build_grid_options(self):
        btns = []

        if self.download:
            d_button = self.grid_button(button_type='download', title='Download',
                href=self.ctx.URL('actions', vars={"caller": self.ctx['app_name'], 
                "cdb":self.cdb, "action":"download", "table" : self.table._tablename}))
            btns.append(d_button)
        
        if self.upload:
            u_button = self.grid_button(button_type='upload_csv', title='Upload CSV',
                href=self.ctx.URL('actions', vars={"caller": self.ctx['app_name'], 
                "cdb":self.cdb, "action":"upload", "table" : self.table._tablename}))
            btns.append(u_button)
        
        if self.create:
            a_button = self.grid_button(button_type='create', title="Create",  
                href=self.ctx.URL('actions', vars={"cdb":self.cdb, "caller": self.ctx['app_name'], 
                "table" : self.table._tablename, "action":"create"}))
            btns.append(a_button)
        
        if not self.page_title:
            if not self.table._plural:
                self.page_title=self.table
            else:
                self.page_title = self.table._plural
        return btns
    
    def build_headers(self):
        headers= ''
        db = self.db
        hide = self.hide
        t = self.table
        self.col =  ",".join(self.fields)
        self.columns=[]
        self.labels=[]
        for f in self.fields:
            if f in hide:
                continue
            if f == 'id':
                if self.show_id:
                    self.columns.append({'data': f})
                    self.labels.append(db[t][f].label)
                    continue
                else:
                    continue
            self.columns.append({'data': f})
            self.labels.append(db[t][f].label)
            
        self.labels.append('Actions')
        self.columns.append({'data': 'btns'})
        headers = self.labels
        return headers
    
    def build_row_buttons(self):
        #implemented in subclass as depends on type of grid
        ...
    
    def build_serverside_script(self):
        # implemented in subclass as depends on type of grid
        ...

    def __call__(self,
                ctx=None,
                db = None,
                table = None,
                b_button = None,
                ):
        if ctx :
            self.ctx = ctx
        if db:
            self.db = ctx.ask(db)
        if table:
            self.table = table
        
        if isinstance(self.table, list):
            # mimic a table from a list of fields without calling define_table
            form_name = form_name or 'none'
            for field in self.table: 
                field.tablename = getattr(field,'tablename',form_name)
        else:
            self.fields=self.table.fields
            
        self.build_headers() 
        return self        
