from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class HspotADDForm(FlaskForm):
    hspot = StringField('Enter the code of railway station for adding it to the hotspot list : ', validators=[DataRequired()])
    submit = SubmitField('Submit') 
    


class HspotREMForm(FlaskForm):
    hspotr = StringField('Enter the code of railway station for removing it from hotspot list : ', validators=[DataRequired()])
    submitr = SubmitField('Submit') 
    
class SetradiusForm(FlaskForm):
    setr = StringField('Enter the radius of hotspot you want to consider (in meters) : ', validators=[DataRequired()])
    submit = SubmitField('Submit')

class setthresholdNumForm(FlaskForm):
    setnum = StringField('Enter the threshold number below which station should be consider to made operational :', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SetminimumroutelengthForm(FlaskForm):
    setmrl = StringField('Enter the minimum route length you want to consider :   ', validators=[DataRequired()])
    submit = SubmitField('Submit')
    


class parametersForm(FlaskForm):
    addhspot = StringField('Enter the code of railway station for adding it to the hotspot list : ')
    remhspot = StringField('Enter the code of railway station for removing it from hotspot list : ')
    setr = StringField('Enter the radius of hotspot you want to consider (in meters) : ', validators=[DataRequired()])
    setnum = StringField('Enter the threshold number below which station should be consider to made operational :', validators=[DataRequired()])
    setmrl = StringField('Enter the minimum route length you want to consider :   ', validators=[DataRequired()])
    submit = SubmitField('Submit')