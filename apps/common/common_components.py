from websaw import DefaultContext
from upytl import (Component,Slot, 
                    html as h
)


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
