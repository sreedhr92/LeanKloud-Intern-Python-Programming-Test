from flask import Flask
import mysql.connector
from datetime import date
from flask_restplus import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A simple TodoMVC API',
)
db = mysql.connector.connect(host = "localhost",user="sree",passwd="sree",database="user")


ns = api.namespace('todos', description='TODO operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details'),
    'dueby': fields.Date(required=True, description='The task due date(YYYY-MM-DD)'),
    'status': fields.String(required=True, description='The task status')
    
})


class TodoDAO(object):
    def __init__(self):
        self.todos = []

    def get(self, id):
        cur = db.cursor()
        cur.execute("select * from tasks where id = %s",(id,))
        output = cur.fetchall()
        if len(output)>0:
            tasks = []
            for i in output:
                task = {'id':i[0],'task':i[1],'dueby':i[2],'status':i[3]}
                tasks.append(task)
            cur.close()
            return tasks
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        cur = db.cursor()
        todo = data
        cur.execute("insert into tasks(task,dueby,status) values(%s,%s,%s)",(todo['task'],todo['dueby'],todo['status']))
        db.commit()
        cur.close()
        return todo

    def update(self, id, data):
        cur = db.cursor()
        todo = data
        cur.execute("update tasks set task=%s,dueby=%s,status=%s where id=%s",(todo['task'],todo['dueby'],todo['status'],id))
        db.commit()
        cur.close()
        return todo

    def update_status(self, id, status):
        cur = db.cursor()
        cur.execute("update tasks set status=%s where id=%s",(status,id))
        db.commit()
        cur.execute("select * from tasks where id=%s",(id,))
        output = cur.fetchall()
        tasks = []
        for i in output:
            task = {'id':i[0],'task':i[1],'dueby':i[2],'status':i[3]}
            tasks.append(task)
        cur.close()
        return tasks


    def delete(self, id):
        cur = db.cursor()
        cur.execute("delete from tasks where id=%s",(id,))
        db.commit()
        cur.close()
    
    def getDueTasks(self, date):
        cur = db.cursor()
        cur.execute("select * from tasks where not status ='Finished' and dueby=%s ",(date,))
        output = cur.fetchall()
        tasks = []
        for i in output:
            task = {'id':i[0],'task':i[1],'dueby':i[2],'status':i[3]}
            tasks.append(task)
        cur.close()
        return tasks
    
    def getOverDueTasks(self):
        cur = db.cursor()
        today = date.today()
        cur.execute("select * from tasks where dueby < %s and not status ='Finished'",(today,))
        output = cur.fetchall()
        tasks = []
        for i in output:
            task = {'id':i[0],'task':i[1],'dueby':i[2],'status':i[3]}
            tasks.append(task)
        cur.close()
        return tasks
    
    def getFinishedTasks(self):
        cur = db.cursor()
        cur.execute("select * from tasks where status ='Finished'")
        output = cur.fetchall()
        tasks = []
        for i in output:
            task = {'id':i[0],'task':i[1],'dueby':i[2],'status':i[3]}
            tasks.append(task)
        cur.close()
        return tasks

    


DAO = TodoDAO()
'''DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})'''


@ns.route('/')
@ns.response(201, 'Operation Success')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        cur = db.cursor()
        cur.execute("select * from tasks")
        output = cur.fetchall()
        tasks = []
        for i in output:
            task = {'id':i[0],'task':i[1],'dueby':i[2],'status':i[3]}
            tasks.append(task)
        cur.close()
        return tasks

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)



@ns.route('/<int:id><string:status>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
@ns.param('status', 'The task status')
class Status(Resource):
    '''Show a single todo item and lets you modify its status'''

    @ns.doc('change_status_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id,status):
        '''Update a task's status given its identifier'''
        return DAO.update_status(id, status)

@ns.route('/due/<date>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
@ns.param('date', 'Date of the task(YYYY-MM-DD)')
class Due(Resource):
    '''Shows the list of all todo's which are due to be finished on that specific date'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, date):
        '''Fetch the list of all todo's which are due to be finished '''
        return DAO.getDueTasks(date)

@ns.route('/overdue')
@ns.response(404, 'Todo not found')
class Overdue(Resource):
    '''Shows the list of all todo's which are passed their due date'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        '''Fetch the list of all todo's which are passed their due date'''
        return DAO.getOverDueTasks()

@ns.route('/finished')
@ns.response(404, 'Todo not found')
class Finished(Resource):
    '''Shows the list of all todo's which are finished'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self):
        '''Fetch the list of all todo's which are finished'''
        return DAO.getFinishedTasks()

if __name__ == '__main__':
    app.run(debug=True)