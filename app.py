from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
  sno = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  desc = db.Column(db.String(500), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self) -> str:
      return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
  if request.method == 'POST':
    title = request.form['title']
    desc = request.form['desc']
    todo= Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()

  allTodo = Todo.query.all()
  return render_template('index.html', allTodo = allTodo)

@app.route("/show")
def showAll():
  allTodo = Todo.query.all()
  print(allTodo)
  return "this is show page"

@app.route("/Update/<int:sno>", methods=['GET', 'POST'])
def Update(sno):
  if request.method == 'POST':
    title = request.form['title']
    desc = request.form['desc']
    todo = Todo.query.filter_by(sno=sno).first()
    todo.title = title
    todo.desc = desc
    db.session.add(todo)
    db.session.commit()
    return redirect("/")

  todo = Todo.query.filter_by(sno=sno).first()
  return render_template('update.html', todo = todo)

@app.route("/Delete/<int:sno>")
def Delete(sno):
  delTodo = Todo.query.filter_by(sno=sno).first()
  db.session.delete(delTodo)
  db.session.commit()
  return redirect("/")

@app.route("/about")
def about():
  return render_template('about.html')

if __name__ == "__main__":
  app.run(debug=True)