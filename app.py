from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:popo@localhost/todoproject"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))

# Home Route
@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        todoproject = Todo(title=title, description=description)
        db.session.add(todoproject)
        db.session.commit()
        return redirect("/")

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

# Delete Route
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

# Optional route
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    todoproject = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todoproject.title = request.form['title']
        todoproject.description = request.form['desc']
        db.session.commit()
        return redirect('/')  # redirect after successful update

    return render_template('update.html', todoproject=todoproject)

if __name__ == "__main__":
    app.run(debug=True, port=7000)
