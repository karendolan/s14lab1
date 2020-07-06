from flask import Flask, render_template
from sklearn.externals import joblib


app = Flask(__name__)


def doPrediction(test, model, id, name):
    prediction = model.predict(test)[0][0].round(1)
    return {
            'id': id,
            'name': name,
            'prediction': str(prediction)
    }


@app.route("/", methods=['GET', 'POST'])
def index():
    # Make prediction -
    #  features = ['BEDS', 'BATHS', 'SQFT', 'AGE', 'LOTSIZE', 'GARAGE']
    samplePredict = [[4, 2.5, 3005, 15, 17903.0, 1]]
    features = {
        'beds': 4,
        'baths': 2.5,
        'sqft': 3005,
        'age': 15,
        'lotsize': 17903.0,
        'garage': 1,
    }
    # Load ML model
    model = joblib.load('./notebooks/regr.pkl')
    # label = ['SOLDPRICE']
    # features = ['BEDS', 'BATHS', 'SQFT', 'AGE', 'LOTSIZE', 'GARAGE']
    # prediction = model.predict([[4, 2.5, 3005, 15, 17903.0, 1]])[0][0].round(1)
    # prediction = str(prediction)
    model_lr = joblib.load('./notebooks/reg_linearreg_hw1.pkl')
    model_dt = joblib.load('./notebooks/reg_decisiontreereg_hw1.pkl')

    predictions = []
    predictions.append(
        doPrediction(samplePredict, model, 'm', 'orig')
    )
    predictions.append(
        doPrediction(samplePredict, model_lr, 'lr', 'linear regression')
    )
    predictions.append(
        doPrediction(samplePredict, model_dt, 'dt', 'decision tree')
    )
    return render_template(
        'index.html',
        predictions=predictions,
        models=predictions,
        f=features
     )


@app.route('/world')
def hello_world():
    return 'Hello, World!'


@app.route('/<you>')
def hello_you(you):
    return f'Hello, {you}!'
