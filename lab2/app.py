from flask import Flask, render_template
from sklearn.externals import joblib

app = Flask(__name__)


def doPrediction(test, model, name):
    prediction = model.predict(test) # [0][0].round(1)
    return {
            'model': name,
            'prediction': str(prediction)
    }



@app.route('/')
def index():
    # Make prediction -
    #  features = ['BEDS', 'BATHS', 'SQFT', 'AGE', 'LOTSIZE', 'GARAGE']
    samplePredict = [[4, 2.5, 3005, 15, 17903.0, 1]]
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
        doPrediction(samplePredict, model, 'orig')
    )
    predictions.append(
        doPrediction(samplePredict, model_lr, 'linear regression')
    )
    predictions.append(
        doPrediction(samplePredict, model_dt, 'decision tree')
    )

    return render_template(
        'index.html',
        predictions=predictions
     )


@app.route('/world')
def hello_world():
    return 'Hello, World!'


@app.route('/<you>')
def hello_you(you):
    return f'Hello, {you}!'
