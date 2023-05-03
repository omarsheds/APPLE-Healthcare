import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt , login_manager
from flaskblog.forms import  AppointmentForm, PatientCheckForm, MedicalForm, RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CheckForm,RegistrationFormDoc,PatientForm
from flaskblog.models import User,  check , Post , medical, appointment
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.Model import classifier
from functools import wraps


#def login_required(role="ANY"):
#    def wrapper(fn):
#        @wraps(fn)
#        def decorated_view(*args, **kwargs):
#            if not current_user.is_authenticated:
#              return login_manager.unauthorized()
#            if ((current_user.role != role) and (role != "ANY")):
#                return login_manager.unauthorized()
#            return fn(*args, **kwargs)
#        return decorated_view
#    return wrapper


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)




@app.route("/about")
def about():
    return render_template('about1.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,role="user")
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role=="user":
            login_user(user, remember=form.remember.data)
            
    
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.number= form.number.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data= current_user.name 
        form.number.data=  current_user.number
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@app.route('/test', methods = ['POST','GET']) 
@login_required
def test():
    form = CheckForm()
    if request.method == 'POST': 
#        to_predict_list = request.form.to_dict() 
#        to_predict_list = list(to_predict_list.values()) 
#        to_predict_list = list(map(int, to_predict_list)) 
#        result = ValuePredictor(to_predict_list)    
#        int_features = [int(x) for x in request.form.values()]
        male=(request.form.get("male"))
        age=(request.form.get("age"))
        education=(request.form.get("education")) 
        smoker =(request.form.get("smoker"))
        cigs=(request.form.get("cigs")) 
        bpmeds=(request.form.get("bpmeds")) 
        prestr=(request.form.get("prestr"))
        prehyp=(request.form.get("prehyp"))
        diabetes=(request.form.get("diabetes"))
        totChol=(request.form.get("totChol")) 
        sysBP=(request.form.get("sysBP"))
        diaBP=(request.form.get("diaBP"))
        BMI = (request.form.get("BMI"))
        heartRate=(request.form.get("heartRate")) 
        glucose=(request.form.get("glucose")) 
        
        array=[[male, age, education,smoker,cigs,bpmeds,prestr,prehyp,diabetes,totChol,sysBP,diaBP,BMI,heartRate,glucose]]
        
        result1 = classifier.predict(array)
        
        test = check(male=form.male.data, age=form.age.data,education=form.education.data,smoker=form.smoker.data,cigs=form.cigs.data,bpmeds=form.bpmeds.data,prestr=form.prestr.data,prehyp=form.prehyp.data,diabetes=form.diabetes.data,totChol=form.totChol.data,sysBP=form.sysBP.data,diaBP=form.diaBP.data,BMI=form.BMI.data,heartRate=form.heartRate.data,glucose=form.glucose.data,result=result1[0],test=current_user)
        
        db.session.add(test)
        
        db.session.commit()
        if result1[0]== 1: 
           return render_template('bad.html', title = "High Risk")
        else: 
           return render_template("good.html" , title = "Low Risk")
        
    return render_template("index.html",form =form)




@app.route("/medicalhistory", methods=['GET', 'POST'])
@login_required
def medicalHistory():
    form = MedicalForm()
    if form.validate_on_submit():
        
        medical.gender = form.gender.data
        medical.blood = form.blood.data
        medical.age = form.age.data
        medical.personal = form.personal.data
        medical.personal2=form.personal2.data
        medical.personal3=form.personal3.data
        medical.family = form.family.data
        medical.family2 = form.family2.data
        medical.family3 = form.family3.data
        medical.al1 = form.al1.data
        medical.al2 = form.al2.data
        medical.al3 = form.al3.data
        medical.med1 = form.med1.data
        medical.med2 = form.med2.data
        medical.med3 = form.med3.data
        medical.smoker = form.smoker.data
        medical.drinker = form.drinker.data
        medical.drugs = form.drugs.data
        test = medical(gender=form.gender.data,blood=form.blood.data, age=form.age.data,personal=form.personal.data,personal2=form.personal2.data,personal3=form.personal3.data,family=form.family.data,family2=form.family2.data,family3=form.family3.data,al1=form.al1.data,al2=form.al2.data,al3=form.al3.data,med1=form.med1.data,med2=form.med2.data,med3=form.med3.data,smoker=form.smoker.data,drinker=form.drinker.data,drugs=form.drugs.data,history=current_user)
        
        db.session.add(test)
        db.session.commit()
        flash('Your medical history has been updated!', 'success')
        return redirect(url_for('medicalHistory'))
    elif request.method == 'GET':
    
        med = medical.query.order_by(-medical.id).filter_by(history=current_user).first()
        if med:
            form.gender.data= med.gender
            form.blood.data= med.blood
            form.age.data=med.age 
            form.personal.data=med.personal 
            form.personal2.data=med.personal2 
            form.personal3.data=med.personal3 
            form.family.data=med.family
            form.family2.data=med.family2
            form.family3.data=med.family3
            form.al1.data=med.al1 
            form.al2.data=med.al2 
            form.al3.data=med.al3
            form.med1.data=med.med1 
            form.med2.data=med.med2
            form.med3.data=med.med3
            form.smoker.data=med.smoker 
            form.drinker.data=med.drinker
            form.drugs.data=med.drugs
            return render_template('medical.html', title='Medical History',
                            form=form)
        else:
            return render_template('medical.html', title='Medical History',
                            form=form)
            
            
            
@app.route("/doctors")
@login_required
def doctors():
    
    page = request.args.get('page', 1, type=int)
    doctor = User.query.order_by(User.discount.desc()).filter_by(role='doctor').paginate(page=page, per_page=5)
   
    return render_template('doctors.html', doctor=doctor)

@app.route("/doctors/<string:user>",methods = ['POST','GET'])
def appoint(user):
    form = AppointmentForm()
    shen = User.query.filter_by(username=user).first_or_404()
    
    if form.validate_on_submit():
        flash('Your Appointment has been set!', 'success')
        test = appointment(date=form.date.data, phone=current_user.number ,code=form.code.data, patient=current_user.username ,doctor=user,reservation=current_user)
        
        db.session.add(test)
        
        db.session.commit()
        return redirect(url_for('doctors'))
    
    return render_template('appointment.html', form=form, user=shen)

@app.route("/services")
def services():
    return render_template('services1.html', title = "Healthcare Services")

@app.route("/partners")
def partners():
    return render_template('partners.html', title = "Partners")

@app.route("/medicalpartners")
def medicalpartners():
    return render_template('medicalpartners.html', title = "Medical Partners")

@app.route("/lifestyle")
def lifestyle():
    return render_template('lifestyle.html', title = "Lifestyle Partners")


from flaskblog import routesDoc