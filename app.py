# ----------------------
# Karen Dolan lab3
# CSCI S-14a 2020
# ----------------------
from flask import Flask, render_template, request, redirect, url_for
from models.user import db, User
from modules.userform import UserForm
# Generate random first names
import names
# Generate random ages
import random

from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jmtzhzdmwytcvu:cab47fd3a7c281d058994c0682321ce0b613c1fc41078174f235e5e9a9f5efde@ec2-34-239-241-25.compute-1.amazonaws.com:5432/d4795eqpl9o1kb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
db.init_app(app)


# @route / - GET, POST
@app.route("/", methods=['GET', 'POST'])
def index():
    # Query all
    users = User.query.all()
    # Iterate and print
    users.sort(key=lambda u: u.user_id)
    return render_template("index.html", users=users)


# @route /getuser/<user_id> - GET
@app.route("/getuser/<user_id>", methods=['GET'])
def getUser(user_id):
    # Query user
    user = User.query.get_or_404(
        user_id,
        description='There is no User with user_id {}'.format(user_id)
    )
    return render_template("index.html", users=[user])


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


# @route /updateuser/<user_id> - GET, POST
@app.route('/updateuser/<user_id>', methods=['GET', 'POST'])
def updateUser(user_id):
    user = User.query.get_or_404(
        user_id,
        description='There is no User with user_id {}'.format(user_id)
    )
    form = UserForm()
    # If GET
    if request.method == 'GET':
        form.age.data = user.age
        form.first_name.data = user.first_name
        return render_template('updateuser.html', form=form, user=user)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            return redirect(url_for(
                'updateUserFromUrl',
                user_id=user_id,
                first_name=first_name,
                age=age
            ))
        else:
            return render_template('updateuser.html', form=form, user=user)


# @route /adduser/<first_name>/<age>
@app.route('/updateuser/<user_id>/<first_name>/<age>')
def updateUserFromUrl(user_id, first_name, age):
    db.session.query(User).\
        filter(User.user_id==user_id).\
        update({"age":age, "first_name": first_name})
    db.session.commit()
    return redirect(url_for('index'))


# @route /generateusers/<count>
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


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
