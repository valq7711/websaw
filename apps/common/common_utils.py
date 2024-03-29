import os

from websaw.base_form import BaseForm
from websaw.base_grid import BaseGrid
from pydal.validators import IS_IN_DB

import datetime

class SQLForm(BaseForm):

    def get_select_options(self, field):
        
        table = self.table
        db = self.db
        myfield={}
        
        q= IS_IN_DB(field._db, field)
        
        if isinstance(field.requires, list):
            rec = None
            for i, j in enumerate(field.requires):
                if not isinstance(q, IS_IN_DB):
                    continue
                else:
                    rec = field.requires[i]
                    break
        else:
            rec = field.requires    
        table = db[rec.ktable]
        format = ''
        try:
            format = db[table]._format[2:-2]
        except:
            format = table._fields[1]    
        
        options = []
        for row in db().select(db[table].id, db[table][format]):
            option = {}
            if row.id == self.vars[field.name]:
                option = dict(option=row[format], value=row.id, is_selected = row.id)
            else:
                option = dict(option=row[format], value=row.id, is_selected = None)
            options.append(option)
                                        
            myfield = dict(name=field.name,
                            label=field.label,
                            type='select',
                            value=self.vars[field.name],
                            error=self.errors.get(field.name, ''),
                            options = options)
        return myfield

    def get_options(self, *args, **kw):
        
        # options expected by concrete upytl form-component goes here
        # so we have common processing logic
        # but can adjust options to different upytl form-components
        
        myfields= []
        all_fields=[]    
        for var in self.vars:
            all_fields.append(self.fields[var])
        
        for field in all_fields:
            if not field.type == 'id':
                if field.type.startswith('reference'):
                    myfield = self.get_select_options(field)
                else:    
                    myfield = dict(name=field.name, label=field.label, type=field.type, value=self.vars[field.name], error=self.errors.get(field.name, ''))
                myfields.append(myfield)
                
            else:
                continue    
        return dict(fields=myfields, flash=self.message)

class SQLGrid(BaseGrid):
        
    def build_row_buttons(self, row):
        r_btns = []
        row_buttons=[]
        if self.links:
            for l in self.links:
                r_btns.append('link')
                row_buttons.append({'name': l['name'], 'cdb':self.cdb, 'caller': self.ctx['app_name'], 'func':l['func'], 'fk':l['fk'],'id':row.id}) 
        
        if self.viewable:
            r_btns.append('view')
            row_buttons.append(
                '<a class="tag is-link is-light is-small" href="%s"><i class="fas fa-search-location"></i>&nbsp; View</a>' % ( self.ctx.URL('actions', vars=dict(action='view', table=self.tablename,id=row.id)))
            )
            
        if self.editable:
            r_btns.append('edit')
            row_buttons.append(
                '<a class="tag is-link is-light is-small" href="%s"><i class="fas fa-cog"></i>&nbsp; Update</a>' % ( self.ctx.URL('actions', vars=dict(action='update', table=self.tablename, id=row.id)))
            )
            
        if self.deletable:
            r_btns.append('delete')
            row_buttons.append(
                '<a class="tag is-link is-light is-small" href="%s"><i class="fas fa-trash"></i>&nbsp; Delete</a>' % ( self.ctx.URL('actions', vars=dict(action='delete', table=self.tablename, id=row.id)))
           )
            
        self.r_buts = ",".join(r_btns)
        return row_buttons

    def build_row_data(self, row):
        db = self.db
        table = self.table
        for col in self.fields:
            if db[table][col].type.startswith('reference'):
                row[col] = db[table][col].represent(row[col], row)
        return row

    def get_options(self, *args, **kw):
        
        # options expected by concrete upytl form-component goes here
        # so we have common processing logic
        # but can adjust options to different upytl form-components
        
        payload = {}
        self.tablename = self.table._tablename
    
        payload['title'] = self.page_title
        payload['grid_buttons']=self.build_grid_options()
        payload['columns'] = self.columns
        payload['labels'] = self.labels
        tablename = self.table._tablename
        payload['name'] = tablename
        
        rows = self.db(self.db[tablename]).select()
        data_rows=[]
        for row in rows:
            test = self.build_row_data(row)
            row_buttons = self.build_row_buttons(row)
            row['actions'] = row_buttons
            data_rows.append(row.as_dict())
        payload['data'] = data_rows
        return payload


class SimpleGrid(BaseGrid):
    
    def build_row_data(self, row):
        db = self.db
        table = self.table
        for col in self.fields:
            if db[table][col].type.startswith('reference'):
                row[col] = db[table][col].represent(row[col], row)
        return row

    def get_options(self, *args, **kw):
        
        # options expected by concrete upytl form-component goes here
        # so we have common processing logic
        # but can adjust options to different upytl form-components
        
        payload = {}
        self.tablename = self.table._tablename
    
        payload['title'] = self.page_title
        payload['grid_buttons']= []
        payload['columns'] = self.columns
        payload['labels'] = self.labels
        tablename = self.table._tablename
        payload['name'] = self.table._tablename
        
        rows = self.db(self.db[tablename]).select()
        data_rows=[]
        for row in rows:
            test = self.build_row_data(row)
            data_rows.append(row.as_dict())
        payload['data'] = data_rows
        return payload
