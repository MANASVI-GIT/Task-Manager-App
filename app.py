from flask import Flask, render_template , request , redirect 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    #db = SQLAlchemy(app)
    db.init_app(app)
    app.app_context().push()
    return app


app=create_app()
class Todo(db.Model):
    sno = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(400) , nullable=False)
    duedate = db.Column(db.DateTime , default=datetime.utcnow)
    desc = db.Column(db.String(600) , nullable=False)
    due_date=db.Column(db.String(300) , nullable=False)
    status = db.Column(db.String(300) , nullable=False)


    def _repr_(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title = request.form['title']
        #duedate = request.form['duedate']
        desc = request.form['desc']
        due_date = request.form['due_date']
        status = request.form['status']
        todo = Todo(title=title , desc=desc , due_date=due_date , status=status)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html' , allTodo=allTodo)
    #return 'Hello, World!'

@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/update/<int:sno>' ,  methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        #duedate = request.form['duedate']
        desc = request.form['desc']
        due_date = request.form['due_date']
        status = request.form['status']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title = title
        #todo.duedate = duedate
        todo.desc = desc
        todo.due_date = due_date
        todo.status = status
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html' , todo=todo)
    

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')




@app.route("/sort")
def user_list():
    todo = Todo.query.order_by(desc(Todo.due_date)).all()
    #print(todo)
    return render_template('index.html', allTodo=todo)



if __name__=="__main__":
    #db.init_app(app)
    #with app.app_context():
    app.run(debug=True , port=8000)

