from flask import Flask, request, url_for, redirect
from sklearn.externals import joblib

app = Flask(__name__)
app.config.from_object("app.config")

# unpickle my model
estimators = {
    'B': joblib.load('models/fitB.pkl'),
    'R': joblib.load('models/fitR.pkl'),
    'K': joblib.load('models/fitK.pkl'),
    'D': joblib.load('models/fitD.pkl'),
    'A': joblib.load('models/fitA.pkl'),
    'P': joblib.load('models/fitP.pkl'),
    'C': joblib.load('models/fitC.pkl'),
    'G': joblib.load('models/fitG.pkl')
}
#target_names = ['setosa', 'versicolor', 'virginica']  ### is this needed?

from .views import *


# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
