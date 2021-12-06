from flask import Flask, render_template, request, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:database28#@localhost/task2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)


"""Creating a model Todo"""
class Todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    status=db.Column(db.Boolean)

"""Funcrtionality to display all the tasks"""
@app.route('/',methods=["GET","POST"])
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template("base.html",todo_list=todo_list)

"""Functionality to add a new todo to the list"""
@app.route("/add",methods=["post"])
def add():
    title=request.form.get("title")
    new_todo = Todo(title=title, status =False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

"""Functionality to update the status of a todo as complete or incomplete"""
@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.status= not todo.status
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:todo_id>",methods=["GET","POST"])
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method=='POST':
        todo.title = request.form.get("title")
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return render_template("edit.html", todo=todo)




"""Functionality to delete the todo from the list"""
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return render_template("edit.html")

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)