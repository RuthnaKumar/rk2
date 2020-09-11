from flask import Flask, render_template, request, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(100))
    date = db.Column(db.DateTime)
@app.route('/',methods=['GET'])
def index():

    todos = Todo.query.all()

    return render_template('google.html',title='RK',todos=todos) 
@app.route('/add/',methods=['POST'])
def add():
    data = request.form['task']
    print(data)
    todo = Todo(task=data,date=datetime.now())
    db.session.add(todo)
    db.session.commit()
    return redirect('/')
@app.route('/delete/<id>/')
def delete(id):
  try: 
    todo = Todo.query.get_or_404(id)

    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
  except Exception as e:
      print(e) 
      return abort(404) 
@app.route('/update/<id>/',methods=['GET','POST'])
def update(id):

  todo = Todo.query.get_or_404(id)

  if request.method == 'POST':

       todo.task = request.form['task']
       db.session.commit()
       return redirect('/')
  else:
       
       todos = Todo.query.all()
       return render_template('google.html',update_todo=todo,title='RK',todos=todos)

if __name__ == '__main__':
    app.run(debug=True)