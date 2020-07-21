from dotenv import load_dotenv
from flask import Flask, flash, \
    render_template, request, \
    url_for, redirect, session
from models.models import Db, User, Post
from forms.forms import SignupForm, LoginForm, NewpostForm
from os import environ
from passlib.hash import sha256_crypt

load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/lab5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = environ.get('SECRET_KEY')
Db.init_app(app)


# GET /
@app.route('/')
@app.route('/index')
def index():
    # Control by login status
    print("againg fist", session)
    if 'username' in session:
        session_user = User.query.filter_by(username=session['username']).first()
        print("heooooo", session_user)
        # posts = Post.query.filter_by(author=session_user.uid).all()
        posts = Db.session.query(Post, User) \
                  .filter(Post.author == session_user.uid) \
                  .filter(Post.author == User.uid).all()

        return render_template('index.html',
                               title='Home',
                               posts=posts,
                               session_username=session_user.username)
    else:
        # all_posts = Post.query.all()
        all_posts = Db.session.query(Post, User) \
                      .filter(Post.author == User.uid).all()
        return render_template('index.html', title='Home', posts=all_posts)


#GET & POST /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Init form
    form = LoginForm()

    # If post
    if request.method == 'POST':

        # Init credentials from form request
        username = request.form['username']
        password = request.form['password']

        # Init user by Db query
        user = User.query.filter_by(username=username).first()
        print('heeloooo login: ', username, password, user)

        # Control login validity
        if user is None or not sha256_crypt.verify(password, user.password):
            flash('Invalid username or password', 'alert-danger')
            return redirect(url_for('login'))
        else:
            session['username'] = username
            return redirect(url_for('index'))

    # If GET
    else:
        return render_template('login.html', title='Login', form=form)


#POST /logout
@app.route('/logout', methods=['POST'])
def logout():
    # Logout
    session.clear()
    return redirect(url_for('index'))


#GET & POST /newpost
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    # Init form
    form = NewpostForm()

    # If POST
    if request.method == 'POST':

        # Init user from poster
        session_user = User.query.filter_by(username=session['username']).first()

        # Init content from form request
        content = request.form['content']

        # Create in DB
        # The post's created_date defaults to NOW()
        new_post = Post(author=session_user.uid, content=content)
        Db.session.add(new_post)
        Db.session.commit()

        return redirect(url_for('index'))

    # If GET
    else:
        return render_template('newpost.html', title='Newpost', form=form)


#GET & POST /signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Init form
    form = SignupForm()

    # IF POST
    if request.method == 'POST':

        # Init credentials from form request
        username = request.form['username']
        password = request.form['password']

        # Init user from Db query
        existing_user = User.query.filter_by(username=username).first()

        # Control new credentials
        if existing_user:
            flash('The username already exists. Please pick another one.',
                  'alert-danger')
            return redirect(url_for('signup'))
        else:
            # The user's created_date defaults to NOW()
            user = User(username=username, password=sha256_crypt.hash(password))
            Db.session.add(user)
            Db.session.commit()
            flash('Congratulations, you are now a registered user!',
                  'alert-success')
            return redirect(url_for('login'))

    # IF POST
    else:
        return render_template('signup.html', title='Signup', form=form)
