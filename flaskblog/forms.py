from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import DateField,StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField ,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
#from wtforms.fields.html5 import DateField

class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired()])
    number = StringField('Phone Number',
                           validators=[DataRequired()])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                           validators=[DataRequired()])
    number = StringField('Phone Number',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
                

class UpdateAccountDocForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                           validators=[DataRequired()])
    number = StringField('Phone Number',
                           validators=[DataRequired()])
    clinic = StringField('Clinic Location',
                           validators=[DataRequired()])
    degree = StringField('Degree',
                           validators=[DataRequired()])    
    price = StringField('Consultation Price (original)',
                           validators=[DataRequired()])  
    discount = StringField('Discount',
                           validators=[DataRequired()])  
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    

    
    
class AppointmentForm(FlaskForm):
    date = DateField('Date of appointment', format='%Y-%m-%d')
 
    code = StringField('Code',  validators=[DataRequired()])
    submit = SubmitField('Confirm')
    

class CheckForm(FlaskForm):
    male=SelectField('Gender',choices=[('','Select Here:'),('0','Female'),('1','Male')], validators=[DataRequired()])
    age=StringField('Age', validators=[DataRequired()])
    education=SelectField('Education Level',choices=[('','Select Here:'),('1','Some High School'),('2','Finished High School'),('3','Some College'),('4','Finished College')], validators=[DataRequired()])
    smoker =SelectField('Are you a smoker?',choices=[('','Select Here:'),('0','Non-smoker'),('1','Smoker')], validators=[DataRequired()])
    cigs=StringField('Average number of cigarettes per day (in numbers only)', validators=[DataRequired()]) 
    bpmeds=SelectField('Are you on blood pressure medications?',choices=[('','Select Here:'),('0','No'),('1','Yes')], validators=[DataRequired()])
    prestr=SelectField('Do you have a stroke?',choices=[('','Select Here:'),('0','No'),('1','Yes')], validators=[DataRequired()])
    prehyp=SelectField('Do you have hypertension?',choices=[('','Select Here:'),('0','No'),('1','Yes')], validators=[DataRequired()])
    diabetes=SelectField('Do you have diabetes?',choices=[('','Select Here:'),('0','No'),('1','Yes')], validators=[DataRequired()])
    totChol=StringField('Cholesterol Level (in mg/dL)', validators=[DataRequired()])
    sysBP=StringField('Systolic Blood Pressure', validators=[DataRequired()])
    diaBP=StringField('Diastolic Blood Pressure', validators=[DataRequired()])
    BMI = StringField('BMI', validators=[DataRequired()])
    heartRate=StringField('Heart Rate (in Beats/Min)', validators=[DataRequired()])
    glucose=StringField('Glucose Level (in mg/dL)', validators=[DataRequired()])
    submit = SubmitField('Check')
    

class RegistrationFormDoc(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                           validators=[DataRequired()])
    number = StringField('Phone Number',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    clinic = StringField('Clinic Location', validators=[DataRequired()])
    degree = StringField('Degree in Medicine ', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
            
            
class PatientForm(FlaskForm):
    patient = StringField('Patient username')
    code = StringField('Code')
    submit= SubmitField('Check Patient History')
    
    
class PatientCheckForm(FlaskForm):      
    patient= StringField('Patient username')
    code = StringField('Code')
    submit= SubmitField('Check Patient Test')


class MedicalForm(FlaskForm):
    gender=SelectField('Gender',choices=[('','Select Here:'),('Male','Male'),('Female','Female')])
    blood =SelectField('Blood Type',choices=[('','Select Here:'),('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')])
   
    age=StringField('Age')
    personal=SelectField('Personal History 1',choices=[('','Select Here:'),('Alcohol/Drug Abuse',' Alcohol/Drug Abuse'),('Asthma','Asthma'),('Cancer','Cancer'),('Emphysema (COPD)','Emphysema (COPD)'),('Depression/Anxiety','Depression/Anxiety'),('Bipolar/Suicidal','Bipolar/Suicidal'),('Diabetes','Diabetes'),('Early Death',' Early Death'),('Heart Disease','Heart Disease'),('High Cholesterol','High Cholesterol'),('High Blood Pressure','High Blood Pressure'),('Kidney Disease','Kidney Disease'),('Stroke','Stroke'),('Thyroid Disease','Thyroid Disease'),('Migraine','Migraine')])
    personal2=SelectField('Personal History 2',choices=[('','Select Here:'),('Alcohol/Drug Abuse',' Alcohol/Drug Abuse'),('Asthma','Asthma'),('Cancer','Cancer'),('Emphysema (COPD)','Emphysema (COPD)'),('Depression/Anxiety','Depression/Anxiety'),('Bipolar/Suicidal','Bipolar/Suicidal'),('Diabetes','Diabetes'),('Early Death',' Early Death'),('Heart Disease','Heart Disease'),('High Cholesterol','High Cholesterol'),('High Blood Pressure','High Blood Pressure'),('Kidney Disease','Kidney Disease'),('Stroke','Stroke'),('Thyroid Disease','Thyroid Disease'),('Migraine','Migraine')])
    personal3=SelectField('Personal History 3',choices=[('','Select Here:'),('Alcohol/Drug Abuse',' Alcohol/Drug Abuse'),('Asthma','Asthma'),('Cancer','Cancer'),('Emphysema (COPD)','Emphysema (COPD)'),('Depression/Anxiety','Depression/Anxiety'),('Bipolar/Suicidal','Bipolar/Suicidal'),('Diabetes','Diabetes'),('Early Death',' Early Death'),('Heart Disease','Heart Disease'),('High Cholesterol','High Cholesterol'),('High Blood Pressure','High Blood Pressure'),('Kidney Disease','Kidney Disease'),('Stroke','Stroke'),('Thyroid Disease','Thyroid Disease'),('Migraine','Migraine')])
    family=SelectField('Family History 1',choices=[('','Select Here:'),('Alcohol/Drug Abuse',' Alcohol/Drug Abuse'),('Asthma','Asthma'),('Cancer','Cancer'),('Emphysema (COPD)','Emphysema (COPD)'),('Depression/Anxiety','Depression/Anxiety'),('Bipolar/Suicidal','Bipolar/Suicidal'),('Diabetes','Diabetes'),('Early Death',' Early Death'),('Heart Disease','Heart Disease'),('High Cholesterol','High Cholesterol'),('High Blood Pressure','High Blood Pressure'),('Kidney Disease','Kidney Disease'),('Stroke','Stroke'),('Thyroid Disease','Thyroid Disease'),('Migraine','Migraine')])
    family2=SelectField('Family History 2',choices=[('','Select Here:'),('Alcohol/Drug Abuse',' Alcohol/Drug Abuse'),('Asthma','Asthma'),('Cancer','Cancer'),('Emphysema (COPD)','Emphysema (COPD)'),('Depression/Anxiety','Depression/Anxiety'),('Bipolar/Suicidal','Bipolar/Suicidal'),('Diabetes','Diabetes'),('Early Death',' Early Death'),('Heart Disease','Heart Disease'),('High Cholesterol','High Cholesterol'),('High Blood Pressure','High Blood Pressure'),('Kidney Disease','Kidney Disease'),('Stroke','Stroke'),('Thyroid Disease','Thyroid Disease'),('Migraine','Migraine')])
    family3=SelectField('Family History 3',choices=[('','Select Here:'),('Alcohol/Drug Abuse',' Alcohol/Drug Abuse'),('Asthma','Asthma'),('Cancer','Cancer'),('Emphysema (COPD)','Emphysema (COPD)'),('Depression/Anxiety','Depression/Anxiety'),('Bipolar/Suicidal','Bipolar/Suicidal'),('Diabetes','Diabetes'),('Early Death',' Early Death'),('Heart Disease','Heart Disease'),('High Cholesterol','High Cholesterol'),('High Blood Pressure','High Blood Pressure'),('Kidney Disease','Kidney Disease'),('Stroke','Stroke'),('Thyroid Disease','Thyroid Disease'),('Migraine','Migraine')])

    al1=StringField('Drug Allergies 1')
    al2=StringField('Drug Allergies 2')
    al3=StringField('Drug allergies 3')
    med1=StringField('Current Medications 1')
    med2=StringField('Current Medications 2')
    med3=StringField('Current Medications 3')
    smoker =SelectField('Are you a smoker?',choices=[('','Select Here:'),('Non-smoker','No'),('Smoker','Yes'),('Smoked in the past but stopped now','Former Smoker')])
    drinker =SelectField('History with alcohol?',choices=[('','Select Here:'),('No Alcohol-history','I have no history with Alcohol'),('I regularly consume alcohol','I regularly consume alcohol'),('I used to drink in the past but stopped now','I used to drink in the past but stopped now')])
    drugs =SelectField('History with illegal drugs?',choices=[('','Select Here:'),('No drug-history','I have no history with illegal drugs'),('I regularly consume illegal drugs','I regularly consume illegal drugs'),('I used to consume drugs but stopped','I used to consume drugs but stopped')])
    submit = SubmitField('Save')
    
    
    
class verifyForm(FlaskForm):      
    submit= SubmitField('Verify')
