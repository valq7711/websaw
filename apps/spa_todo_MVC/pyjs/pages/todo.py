from pyjsaw.typing.jstyping import JSON, RegExp

from pyjsaw.js_stuff.vuestuff import VTempl, VDot as v
from pyjsaw.js_stuff import html as h, template
from pyjsaw.pyjs.vcollector import vc


templ = VTempl({
    h.Div():{
        h.Section(Class='todoapp'):{
            h.Header(Class='header'):{
                h.H1():'Todos',
                h.Input(
                    v.on({'keyup.enter':'addTodo'}),
                    autofous='autofocus',
                    placeholder="What needs to be done?",
                    Class='new-todo'
                ):'',
            },
            h.Section(v.Show('todos.length'), Class='main'):{
                h.Input(        
                    v.bind(checked="remaining == 0"),
                    v.On(change='toggleAll'),
                    id="toggle-all",
                    Class='toggle-all',
                    type = 'checkbox'):'',

                h.Label(For='toggle-all'):'Mart all as complete',
                h.UL(Class='todo-list'):{
                    h.LI(
                        v.For("todo in filteredTodos"),
                        v.bind(key='todo.id'),
                        v.bind(Class="{ completed: todo.completed, editing: todo == editedTodo }"),
                        Class = 'todo'
                    ):{
                        h.Div(Class='view'):{
                            h.Input(
                                v.model('todo.completed'),
                                type = 'checkbox',
                                Class = 'toggle'):'',

                            h.Label(v.On(dblclick='editTodo(todo)')):'{{todo.title}}',
                            h.Button(v.On(click='removeTodo(todo)'), Class='destroy'):'',
                            
                        },
                        h.Input(
                            v.model('todo.title'),
                            v.If("todo == editedTodo"),
                            v.On({'vnode-mounted':"el.focus()"}),
                            v.On({'keyup.enter':'doneEdit(todo)'}),
                            v.On({'keyup.escape':'cancelEdit(todo)'}),
                            v.On(blur = 'doneEdit(todo)'),
                            Class='edit',
                            Type='text'):'',
                    }
                }
            },
            h.Footer(v.Show("todos.length"), Class="footer"):{
                h.Span(Class='todo-count'):'{{remaining}} {{ remaining == 1 ? " item" : " items"  }} left',
                h.UL(Class='filters'):{
                    h.LI():{
                        h.A(v.bind(Class="{ selected: visibility == 'all' }"),href="#/all"):'All',
                    },    
                    h.LI():{
                        h.A(v.bind(Class="{ selected: visibility == 'active' }"), href="#/active"):'Active',
                    },
                    h.LI():{
                        h.A(v.bind(Class="{ selected: visibility == 'completed' }"), href="#/completed"):'Completed',
                    },
                    h.Button(v.On(click="removeCompleted"), v.Show('todos.length > remaining'),Class='clear-completed'):'Clear completed'
                }
            }
        }
    }
})


# The filter function could equally well be done as a series of lambdas but is split out here in order 
# to demonstrate how to handle nested vue callback type functions in pyjsaw.
# These should be OUTSIDE of the scope of the class as below 
"""
const filters = {
  all: (todos) => todos,
  active: (todos) => todos.filter((todo) => !todo.completed),
  completed: (todos) => todos.filter((todo) => todo.completed)
}
"""

def filter(data, key):
    
    filtered = []
    
    if key == 'all':
        return data
    
    if key == 'active':
        for rec in data:
            if rec['completed'] == False:
                filtered.push(rec)
        return filtered
    
    if key == 'completed':
        for rec in data:
            if rec['completed'] == True:
                filtered.push(rec)
        return filtered
    
    
# This is the key as set by the main index controller in the inital app_state

STORAGE_KEY = 'spa_todo_mvc'

@vc.component()
class Todo:
    
    template = templ

    def data(data_obj, vm: 'Todo'):
        data_obj.todos = JSON.parse(localStorage.getItem(STORAGE_KEY) or '[]')
        data_obj.editedTodo = None
        data_obj.visibility = 'all'
    
    # watch todos change for localStorage persistence
    
    @vc.watch('todos')
    def todos(self, n, o):
        localStorage.setItem(STORAGE_KEY, JSON.stringify(n))
    
    def mounted(self):
        
        # note that we are using the function here as opposed to self.onHashChange()
        window.addEventListener('hashchange', self.onHashChange)
        self.onHashChange()
  
    @vc.computed
    def filteredTodos(self):
        return filter(self.todos, self.visibility)
        
    @vc.computed
    def remaining(self):
        data = self.todos
        filtered = filter(data, 'active')
        if filtered:
            return filtered.length
        else:
            return 0
    
    def toggleAll(self, e):
        todos = self.todos
        for t in todos:
            t.completed = e.target.checked
    
    def addTodo(self, e):
        value = e.target.value.trim()
        if not value:
            return
        self.todos.push({
            'id': Date.now(),
            'title': value,
            'completed': False
        })
        e.target.value = ''

    def removeTodo(self,todo):
        self.todos.splice(self.todos.indexOf(todo), 1)

    def editTodo(self, todo):
        self.beforeEditCache = todo.title
        self.editedTodo = todo

    def doneEdit(self, todo):
        if not self.editedTodo:
            return
        self.editedTodo = None
        todo.title = todo.title.trim()
        if not todo.title:
            self.removeTodo(todo)
    
    def removeCompleted(self):
        data = self.todos
        self.todos = filter(data, 'active')
    
    def cancelEdit(self, todo):
        self.editedTodo = None
        todo.title = self.beforeEditCache
    
    def onHashChange(self):
       
        # Original code : var visibility = window.location.hash.replace(/#\/?/, '')
        # python does not have a literal for regexp so we use the following
        # note: we do not need to escape the / 
        
        visibility = window.location.hash.replace(RegExp('#/?'), '')
 
        data = filter(self.todos, visibility)
        if data:
            self.visibility = visibility
        else:
            window.location.hash = ''
            self.visibility = 'all'
    
def make():
    return Todo
