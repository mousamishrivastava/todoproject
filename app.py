from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ SQLite DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todoproject.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

# ✅ Create tables on app start (Render needs this)
with app.app_context():
    db.create_all()

# ✅ Home Route
@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['desc']
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect("/")

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

# ✅ Delete Route
@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('hello_world'))

# ✅ Update Route
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['desc']
        db.session.commit()
        return redirect('/')

    return render_template('update.html', todoproject=todo)

# ✅ Run the app locally
if __name__ == "__main__":
    app.run(debug=True, port=7000)
