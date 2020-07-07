# ----------------------
# Karen Dolan lab2
# CSCI S-14a 2020
# ----------------------
from flask import Flask, render_template, request
# from sklearn.externals import joblib
import joblib

app = Flask(__name__)

# Model import constants
modelDict = {
  'lr': {
    'name': 'Linear Regression (normalized inputs)',
    'path': './lab2/notebooks/regr.pkl',
    'model': None,
    'id': 'lr',
  },
  'rg': {
    'name': 'Ridge Regression',
    'path': './lab2/notebooks/reg_ridge_hw1.pkl',
    'model': None,
    'id': 'rg',
  },
  'dt': {
    'name': 'Decision Tree',
    'path': './lab2/notebooks/reg_decisiontreereg_hw1.pkl',
    'model': None,
    'id': 'dt',
  }
}


# lab2 - retrieve model package
def getModel(modelId):
    model = modelDict[modelId]
    if not model['model']:
        model['model'] = joblib.load(model['path'])
    return model


# lab2 - perform prediction
def doPrediction(test, model):
    # Some models reqired ravelled y values
    try:
        prediction = model['model'].predict(test)[0][0].round(2)
    except IndexError:
        prediction = model['model'].predict(test)[0].round(2)
    return {
            'id': model['id'],
            'name': model['name'],
            'value': str(prediction)
    }

# from lab2 -  form posts back
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.form:
        features = request.form
        try:
            modelId = request.form['model']
        except KeyError:
            modelId = 'dt'
    else:
        features = {
            'beds': 4,
            'baths': 2.5,
            'sqft': 3005,
            'age': 15,
            'lotsize': 17903.0,
            'garage': 1,
        }
        modelId = 'dt'
    # Make prediction -
    #  features = ['BEDS', 'BATHS', 'SQFT', 'AGE', 'LOTSIZE', 'GARAGE']
    # samplePredict = [[4, 2.5, 3005, 15, 17903.0, 1]]
    predictVector = [[
        float(features['beds']),
        float(features['baths']),
        float(features['sqft']),
        float(features['age']),
        float(features['lotsize']),
        float(features['garage'])
    ]]
    # modelId
    model = getModel(modelId)
    prediction = doPrediction(predictVector, model)
    return render_template(
        'index.html',
        prediction=prediction,
        models=modelDict.values(),
        f=features
     )

# from lab1
@app.route('/world')
def hello_world():
    return 'Hello, World!'

# from lab1
@app.route('/<you>')
def hello_you(you):
    return f'Hello, {you}!'
