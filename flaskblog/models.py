from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin,current_user



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    checks = db.relationship('check', backref='test', lazy=True)
    medical =db.relationship('medical', backref='history', lazy=True)
    appointments =db.relationship('appointment', backref='reservation', lazy=True)
    degree = db.Column(db.String(60), nullable=False)
    clinic = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Integer(), nullable=True)
    discount =db.Column(db.Integer(), nullable=True)
    number =db.Column(db.Integer(), nullable=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), unique=True, nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
    
class appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(60), nullable=False)
    phone= db.Column(db.String(60), nullable=False)
    code = db.Column(db.String(60), nullable=False)
    patient = db.Column(db.String(60), nullable=False, default="None")
    doctor = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
    def __repr__(self):
        return f"appointment('{self.date}', '{self.patient}')"
    
    
    
    


class check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    male=db.Column(db.String(60), nullable=False)
    age=db.Column(db.String(60), nullable=False)
    education=db.Column(db.String(60), nullable=False)
    smoker =db.Column(db.String(60), nullable=False)
    cigs=db.Column(db.String(60), nullable=False)
    bpmeds=db.Column(db.String(60), nullable=False)
    prestr=db.Column(db.String(60), nullable=False)
    prehyp=db.Column(db.String(60), nullable=False)
    diabetes=db.Column(db.String(60), nullable=False)
    totChol=db.Column(db.String(60), nullable=False)
    sysBP=db.Column(db.String(60), nullable=False)
    diaBP=db.Column(db.String(60), nullable=False)
    BMI = db.Column(db.String(60), nullable=False)
    heartRate=db.Column(db.String(60), nullable=False)
    glucose=db.Column(db.String(60), nullable=False)
    result=db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"check('{self.result}')"
    
    
    
class medical(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender=db.Column(db.String(60), nullable=True, default="None")
    blood=db.Column(db.String(60), nullable=True, default="None")
    age=db.Column(db.String(60), nullable=True, default="None")
    personal=db.Column(db.String(300), nullable=True, default="None")
    personal2=db.Column(db.String(300), nullable=True, default="None")
    personal3=db.Column(db.String(300), nullable=True, default="None")
    family=db.Column(db.String(300), nullable=True, default="None")
    family2=db.Column(db.String(300), nullable=True, default="None")
    family3=db.Column(db.String(300), nullable=True, default="None")
    al1=db.Column(db.String(60), nullable=True, default="None")
    al2=db.Column(db.String(60), nullable=True, default="None")
    al3=db.Column(db.String(60), nullable=True, default="None")
    med1=db.Column(db.String(60), nullable=True, default="None")
    med2=db.Column(db.String(60), nullable=True, default="None")
    med3=db.Column(db.String(60), nullable=True, default="None")
    smoker =db.Column(db.String(60), nullable=True, default="None")
    drinker =db.Column(db.String(60), nullable=True, default="None")
    drugs=db.Column(db.String(60), nullable=True, default="None")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"medicalHistory('{self.gender}','{self.age}','{self.personal}','{self.family}','{self.al1}','{self.al2}','{self.al3}','{self.med1}','{self.med2}','{self.med3}','{self.smoker}','{self.drinker}','{self.drugs}')"
    
    
    
