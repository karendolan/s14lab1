# ----------------------
# Karen Dolan lab3
# CSCI S-14a 2020
# ----------------------
from flask import Flask, render_template, request, redirect, url_for
from models.user import db, User
from modules.userform import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/usersdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
db.init_app(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    # Query all
    users = User.query.all()
    # Iterate and print
    for user in users:
        User.toString(user)
    return render_template("index.html", users=users)


# @route /adduser - GET, POST
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)


# @route /adduser/<first_name>/<age>
@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    db.session.add(User(first_name=first_name, age=age))
    db.session.commit()
    return redirect(url_for('index'))

    # @route /removeuser/<id>
    @app.route('/removeuser/<id>')
    def removeUserFromUrl(id):
        db.session.add(User(first_name=first_name, age=age))
        db.session.commit()
        return redirect(url_for('index'))