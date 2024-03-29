#from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_heroku import Heroku
from models.homeworkuser import Db, HomeworkUser
from os import environ

#load_dotenv('.env') # Can't get this working on Heroku

app = Flask(__name__)
heroku = Heroku(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/homework_users_db'
# WARNING: The heroku ec2 path is needed to connect to heroku db, the heroku = Heroku(app) above is not working, sqlalchemy returns KeyError
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gjejbvcubygmky:311c93a986d4e735a7156908501e72dcd1f29bdb2cc9631f3190d02160d0ad94@ec2-52-202-66-191.compute-1.amazonaws.com:5432/d56fq67s9623r0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
# Can't get the env key working on Heroku
#app.secret_key = environ.get('SECRET_KEY')
Db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/load_data', methods=['GET'])
def load_data():
    users_json = {'users': []}
    users = HomeworkUser.query.all()
    for user in users:
        user_info = user.__dict__
        del user_info['_sa_instance_state']
        users_json['users'].append(user_info)
    return jsonify(users_json)
