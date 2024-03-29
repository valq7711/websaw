import os

class BaseForm:
    def __init__(
        self,
        fields = None,
        validation=None,
    ):
        self.fields = fields
        self.validation = validation
        self.vars = {}
        self.errors = {}
        self.accepted = False
        self.record = None
        self.record_id = None
        self.files = None
        self.message = ''
        self.ctx = None

        
    @staticmethod
    def _get_value(payload, key):
        is_omitted = key not in payload
        multidict = True
        getter = getattr(payload, 'getall', '')
        if not getter:
            multidict = False
            getter = payload.get
        v = getter(key)
        if multidict and isinstance(v, list):
            if v:
                if len(v) == 1:
                    v = v[0]
            else:
                v = None
        return v, is_omitted
    
    def get_options(self):
        # not implemented
        ...
    
    def process(self, ctx, db, table, rec):
        self.db = db
        self.table = table
        if ctx.request.method == 'POST':
            if self.__call__(ctx.request.json or ctx.request.POST, record_id = rec and rec.id).accepted:   
                if isinstance(self.fields, list):
                    return self
                
                if not rec:
                    ret = self.insert(self.table)
                    if ret:
                        self.message = 'Successfully inserted record in db'
                else:
                    if self.update(record = rec):
                        db.commit()
                        self.message = 'Successfully updated record in db'
        
        if ctx.request.method == 'GET':
            if rec:
                if self.__call__(rec.as_dict(), record_id = rec and rec.id).accepted:   
                    return self
                else:
                    print('We need to do something here')    
            else:
                if self.__call__(None, record_id = rec and rec.id).accepted:   
                    return self
                else:
                    print('We need to do something here')    
        return self
    
    def __call__(self, payload, record = None, record_id = None):
        self.record = record
        record_id = self.record_id = record_id or record and record.get("id")
        validated_vars = {}
        self.files = []
        for field in self.fields:
            if not field.writable:  
                continue
            if payload:
                raw_value, is_omitted = self._get_value(payload, field.name)
            else:
                raw_value = ''
                is_omitted = False
            
            self.vars[field.name]  = raw_value
            if field.type == 'upload' and isinstance(raw_value, str):
                value, error = field.validate('', record_id)
                value = raw_value
            else:
                if payload:
                    value, error = field.validate(raw_value, record_id)
                else:
                    value = raw_value
                    error = None
            if error:
                self.errors[field.name] = error
                continue
            if is_omitted:
                continue
            if value is not None:
                if field.type == "upload":
                    self.files.append((field, value))
            validated_vars[field.name] = value
                
        if self.errors:
            return self

        self.vars.update(validated_vars)
        if record_id is not None:
            self.vars["id"] = record_id
        if self.validation:
            self.validation(self)
        if self.errors:
            return self
        self.accepted = True
        return self

    def upload(self, default_folder = None, forced_folder = None):
        if not self.accepted:
            raise RuntimeError('payload is not accepted')
        uploaded = []
        for field, storage in self.files:
            print('Field', field, 'Upload folder', field.uploadfolder, 'Storage', storage.file, storage.filename)
            value = field.store(
                storage.file, storage.filename, forced_folder or field.uploadfolder or default_folder
            )
            uploaded.append(value)
        self.vars[field.name] = uploaded if len(uploaded)>1 else uploaded[0]
    
    def update(self, table = None, record = None, record_id = None, query = None, del_files = False):
        if not self.accepted:
            raise RuntimeError('payload is not accepted')
        record = record or self.record
        if not table and record:
            rec_op = getattr(record or self.record, 'update_record', None)
            if rec_op:
                table = rec_op.db[rec_op.tablename]
                record_id = rec_op.id
        if not (table and (record_id or query)):
            raise RuntimeError('too few arguments')

        vars = table._filter_fields(self.vars)
        if not vars:
            return
        db = table._db
        if record_id:
            q = table._id == record_id
        elif query:
            q = query

        upload_fields_to_del = []
        for k in list(vars.keys()):
            if table[k].type == 'upload':
                if not vars[k]:
                    del vars[k]
                else:
                    upload_fields_to_del.append(table[k])
                    if vars[k] == ':delete':
                        self.vars[k] = vars[k] = ''

        if not vars:
            return
        if del_files and upload_fields_to_del:
            rows = db(q).select(*upload_fields_to_del)
            for r in rows:
                for fld in upload_fields_to_del:
                    fname = r[fld.name]
                    if fname != vars[fld.name]:
                        fp = os.path.join(fld.uploadfolder, fname)
                        if os.path.isfile(fp):
                            os.remove(fp)
        db(q).update(**vars)
        if record:
            record.update(**vars)
            return record.id

    def insert(self, table):
        if not self.accepted:
            raise RuntimeError('payload is not accepted')
        vars = {
            k: v for k, v in table._filter_fields(self.vars).items()
            if table[k].type != 'upload' or v and v[0] != ':'
        }
        id = self.vars["id"] = table.insert(**vars)
        db = self.db
        db.commit()
        return id
