
from flask import render_template
from flask_wtf import Form
from wtforms import fields, TextField, BooleanField, RadioField
from wtforms.validators import Required
import pandas as pd
import numpy as np


from . import app, estimators

class SimpleForm(Form):
    myChoices = [] #<--  needed? ["one", "two", "three", "four"] on Iris
    q81 = RadioField('How much do you go \'clubbing\' (out dancing in bars)?', choices=[('1','Lots'),('2','Never'),('3','Rarely'),('4','Sometimes')])
    q79 = RadioField('What\'s your relationship with marijuana?', choices=[('1','I smoke occasionally'),('2','I smoke regularly'),('3','I smoked in the past, but no longer'),('4','Never')])
    q77 = RadioField('How frequently do you drink alcohol', choices=[('1','Never'),('2','Rarely'),('3','Sometimes'),('4','Very often')])
    q66506 = RadioField('How important to you is a potential match\'s sense of humor?', choices=[('1','Not important'),('2','Somewhat important'),('3','Very important')])
    q60100 = RadioField('Is astrological sign at all important in a match?', choices=[('1','No'),('2','Yes')])
    q43261 = RadioField('How much influence or control do your parents have over your life?', choices=[('1','I almost always do what my parents think is best'),('2','I always do what my parents say'),('3','I am my own person'),('4','I consider their opinion but go my own way')])
    q4018 = RadioField('Are you happy with your life?', choices=[('1', 'No'),('2','Yes')])
    q393 = RadioField('Is there a such thing as having had too many sex partners?', choices=[('1','No'),('2','Yes')])
    q37693 = RadioField('Would you be willing to date someone who plays video games almost every day, for at least 2 hours?', choices=[('1','No.'),('2','Yes, I\'d be playing with them.'),('3','Yes, but I don\'t like video games.'),('4','Yes, but I would not play that much.')])
    q358084 = RadioField('Do you enjoy intense intellectual conversations?', choices=[('1','No'),('2','Yes')])
    q35 = RadioField('Regardless of future plans, what\'s more interesting to you right now?', choices=[('1','Love'),('2','Sex')])
    q274 = RadioField('What\'s the highest level of education you\'ve completed?', choices=[('1','College'),('2','Graduate School'),('3','High School'),('4','Junior High')])
    q19874 = RadioField('How long do your romantic relationships usually last?', choices=[('1','0-6 months'),('2','12+ months'),('3','6-12 months'),('4','I\'ve never been in a relationship')])
    q1597 = RadioField('Would you consider sleeping with someone on the first date?', choices=[('1','No'),('2','Yes')])
    q15280 = RadioField('Could you date someone with no long-term goals?', choices=[('1','No'),('2','Yes')])
    q136 = RadioField('Would you get upset if your girlfriend/boyfriend flirted in front of you?', choices=[('1','No'),('2','Yes')])
    q123 = RadioField('Would you strongly prefer to go out with someone of your own skin color / racial background?', choices=[('1','No'),('2','Yes')])
    q1128 = RadioField('Would you date someone who was already in a committed relationship with someone else?', choices=[('1','No,_but_I_don\'t_think_it\'s_inherently_wrong'),('2','No, it\'s wrong'),('3','Yes,_but_only_if_everybody_knew'),('4','Yes, even in secret')])
    q1062 = RadioField('How frequently do you bathe or shower?', choices=[('1','A couple times a week'),('2','At least once a day'),('3','Once a week or less'),('4','Usually daily. I skip some')])
    q18698 = RadioField('A little grade 10 science. Ideal Gas Law?', choices=[('1','G + V = 1/T'),('2','Not sure / wish I could skip this one'),('3','PV = nRT'),('4','y=mx+b')])

    submit = fields.SubmitField('Submit')


@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    form = SimpleForm()
    my_prediction = None

    if form.validate_on_submit() is False:
        print(form.errors)
    else:
        # store the submitted values
        submitted_data = form.data
        print(submitted_data)

        # Retrieve values from form
        q81 = submitted_data['q81']
        q79 = submitted_data['q79']
        q77 = submitted_data['q77']
        q66506 = submitted_data['q66506']
        q60100 = submitted_data['q60100']
        q43261 = submitted_data['q43261']
        q4018 = submitted_data['q4018']
        q393 = submitted_data['q393']
        q37693 = submitted_data['q37693']
        q358084 = submitted_data['q358084']
        q35 = submitted_data['q35']
        q274 = submitted_data['q274']
        q19874 = submitted_data['q19874']
        q1597 = submitted_data['q1597']
        q15280 = submitted_data['q15280']
        q136 = submitted_data['q136']
        q123 = submitted_data['q123']
        q1128 = submitted_data['q1128']
        q1062 = submitted_data['q1062']
        q18698 = submitted_data['q18698']

        # convert cardinal response to binary array
        def encode(n):
            n = int(n)
            result = np.zeros(4)
            result[n-1] = 1
            return result

        # Create array from values

        responseVector = [encode(q) for q in [q81,q79,q77,q66506,q60100,q43261,q4018,q393,q37693,q358084,q35,q274,q19874,q1597,q15280,q136,q123,q1128,q1062,q18698]]
        responseVector = np.array(responseVector).flatten()
        print(responseVector) # my code
        #my_prediction = str(list(responseVector))
        predictions_vector = [np.round(estimators['B'].predict_proba([responseVector])[0][0]*100),
                              np.round(estimators['K'].predict_proba([responseVector])[0][0]*100),
                              np.round(estimators['R'].predict_proba([responseVector])[0][1]*100),
                              np.round(estimators['D'].predict_proba([responseVector])[0][0]*100),
                              np.round(estimators['A'].predict_proba([responseVector])[0][0]*100),
                              np.round(estimators['P'].predict_proba([responseVector])[0][0]*100),
                              np.round(estimators['C'].predict_proba([responseVector])[0][1]*100),
                              np.round(estimators['G'].predict_proba([responseVector])[0][0]*100),]
        predictionB = 'Probability that you have tried harder drugs (stuff beyond pot): '+str(predictions_vector[0])+'%. '
        predictionK = ' Probability that you are female: '+str(predictions_vector[1])+'%. '
        predictionR = ' Probability that you would be open to an open relationship: '+str(predictions_vector[2])+'%. '
        predictionD = ' Probability that you would google someone before your first date: '+str(predictions_vector[3])+'% '
        predictionA = ' Probability that art is important to you: '+str(predictions_vector[4])+'% '
        predictionP = ' Probability that you were picked on a lot in school: '+str(predictions_vector[5])+'% '
        predictionC = ' Probability that you spend more money on clothes over food: '+str(predictions_vector[6])+'% '
        predictionG = ' Probability that you would date someone that kept a gun in the house: '+str(predictions_vector[7])+'% '

    return render_template('index.html',
        form=form,
        prediction1=predictionB,
        prediction2=predictionK,
        prediction3=predictionR,
        prediction4=predictionD,
        prediction5=predictionA,
        prediction6=predictionP,
        prediction7=predictionC,
        prediction8=predictionG
        )  ## This needs to be specified *****
