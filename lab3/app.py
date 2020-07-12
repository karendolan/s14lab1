# ----------------------
# Karen Dolan lab3
# CSCI S-14a 2020
# ----------------------
from flask import Flask, render_template, request, redirect, url_for
from models.user import db, User
from modules.userform import UserForm
# https://pypi.org/project/names/
import names
import random

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
@app.route('/removeuser/<user_id>')
def removeUserFromUrl(user_id):
    # Query user
    user = User.query.get_or_404(
        user_id,
        description='There is no User with user_id {}'.format(user_id)
    )
    # Delete user
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

# @route /adduser/<first_name>/<age>
@app.route('/updateuser/<user_id>/<first_name>/<age>')
def updateUserFromUrl(user_id, first_name, age):
    db.session.query(User).\
        filter(User.user_id==user_id).\
        update({"age":age, "first_name": first_name})
    db.session.commit()
    return redirect(url_for('index'))


# @route /adduser/<first_name>/<age>
@app.route('/generateusers/<count>')
def randomGenerateUsers(count):
    if(not count.isnumeric()):
        return redirect(url_for('index'))

    for x in range(0, int(count)):
        first_name = names.get_first_name()
        age = random.randint(0, 140)
        db.session.add(User(first_name=first_name, age=age))
        db.session.commit()
    return redirect(url_for('index'))
