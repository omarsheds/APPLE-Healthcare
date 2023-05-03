import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import  verifyForm,PatientCheckForm, MedicalForm, RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CheckForm,RegistrationFormDoc,PatientForm, UpdateAccountDocForm
from flaskblog.models import User,  check , Post , medical , appointment
from flask_login import login_user, current_user, logout_user , login_required
from flaskblog.Model import dataset
from flaskblog import routes

@app.route("/homedoc", methods=['GET', 'POST'])
@login_required
def homeDoc():
    page = request.args.get('page', 1, type=int)
    appointments = appointment.query.order_by(appointment.id.desc()).filter_by(doctor=current_user.username).paginate(page=page, per_page=5)
    
    return render_template('homeDoc.html', appointments=appointments)

@app.route("/aboutdoc")
def aboutdoc():
    return render_template('aboutdoc.html', title='About')


@app.route("/registerdoc", methods=['GET', 'POST'])
def registerDoc():
    if current_user.is_authenticated:
        return redirect(url_for('homeDoc'))
    form = RegistrationFormDoc()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, clinic=form.clinic.data,degree=form.degree.data, password=hashed_password,name=form.name.data,number=form.number.data,role='doctor')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('loginDoc'))
    return render_template('registerDoc.html', title='Register', form=form)

@app.route("/logindoc", methods=['GET', 'POST'])
def loginDoc():
    if current_user.is_authenticated:
        return redirect(url_for('homeDoc'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.role=="doctor":
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homeDoc'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginDoc.html', title='Login', form=form)

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

@app.route("/accountdoc", methods=['GET', 'POST'])
@login_required
def accountDoc():
    form = UpdateAccountDocForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.price = form.price.data
        current_user.discount = form.discount.data
        current_user.number = form.number.data
        current_user.clinic = form.clinic.data
        current_user.degree = form.degree.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data=current_user.name
        form.number.data=current_user.number
        form.clinic.data=current_user.clinic
        form.degree.data=current_user.degree 
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.price.data = current_user.price
        form.discount.data = current_user.discount
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('accountDoc.html', title='Account',
                           image_file=image_file, form=form)
    
@app.route("/checkmedical", methods=['GET', 'POST'])
@login_required
def checkMedical():    
    form = PatientForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(username=form.patient.data).first()
        cod = cod = appointment.query.filter_by(code=form.code.data).filter_by(doctor=current_user.username).first()
        if user and cod:
           med = medical.query.order_by(-medical.id).filter_by(history=user).first()
           if med:
                one= med.gender
                two= med.blood
                three=med.age 
                four=med.personal 
                four2=med.personal2 
                four3=med.personal3 
                five=med.family
                five2=med.family2
                five3=med.family3
                six=med.al1 
                seven=med.al2 
                eight=med.al3
                nine=med.med1 
                ten=med.med2
                eleven=med.med3
                twelve=med.smoker 
                thirteen=med.drinker
                fourteen=med.drugs
                return render_template('userMedical.html', one=one,two=two,three=three,four=four,four2=four2,four3=four3,five=five,five2=five2,five3=five3,six=six,seven=seven,
                                       eight=eight,nine=nine,ten=ten,eleven=eleven,twelve=twelve,thirteen=thirteen,fourteen=fourteen)
           else:
                 flash('The Following user has not submitted his/her medical record yet', 'danger')
                 return redirect(url_for('checkMedical'))
        else:
            flash('Please check the patient username/Code', 'danger')
            return redirect(url_for('checkMedical'))
        
    return render_template('checkmedical.html',form=form)

@app.route("/checktest", methods=['GET', 'POST'])
@login_required
def checkTest():    
        form= PatientCheckForm() 

        if  form.validate_on_submit():
           user1 = User.query.filter_by(username=form.patient.data).first()
           cod = appointment.query.filter_by(code=form.code.data).filter_by(doctor=current_user.username).first()
           if user1 and cod:
               med1 = check.query.order_by(-check.id).filter_by(test=user1).first()
               if med1:
                    form1=verifyForm()
                    one= med1.male
                    two= med1.age
                    three=med1.education 
                    four=med1.smoker
                    five=med1.cigs 
                    six=med1.bpmeds
                    seven=med1.prestr
                    eight=med1.prehyp
                    nine=med1.diabetes
                    ten=med1.totChol
                    eleven=med1.sysBP
                    twelve=med1.diaBP 
                    thirteen=med1.BMI
                    fourteen=med1.heartRate
                    fifteen=med1.glucose
                    sixteen=med1.result
                    global array
                    array=[[one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen]]
                        
                    
                    return render_template('userCheck.html', one=one,two=two,three=three,four=four,five=five,six=six,seven=seven,
                                           eight=eight,nine=nine,ten=ten,eleven=eleven,twelve=twelve,thirteen=thirteen,fourteen=fourteen,fifteen=fifteen,sixteen=sixteen,form=form1)
               else:
                     flash('The Following user has not submitted any Heart Disease check test yet.', 'danger')
                     return redirect(url_for('checkTest'))
           else:
                flash('Please check the patient username/Code', 'danger')
                return redirect(url_for('checkTest'))
        
        return render_template('checktest.html',form=form)
    
    
    
@app.route("/servicesdoc")
def servicesDoc():
    return render_template('servicesDoc.html', title = "Healthcare Services")

@app.route("/partnersdoc")
def partnersdoc():
    return render_template('partnersdoc.html', title = "Partners")

@app.route("/medicalpartnersdoc")
def medicalpartnersdoc():
    return render_template('medicalpartnersdoc.html', title = "Medical Partners")

@app.route("/lifestyledoc")
def lifestyledoc():
    return render_template('lifestyledoc.html', title = "Lifestyle Partners")

@app.route("/appointment/<int:appointment_id>")
def appointments(appointment_id):
    appoint = appointment.query.get_or_404(appointment_id)
    return render_template('appointments.html', appointment=appoint)

@app.route("/appointment/<int:appointment_id>/delete", methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    appoint = appointment.query.get_or_404(appointment_id)
    if appoint.doctor != current_user.username:
        abort(403)
    db.session.delete(appoint)
    db.session.commit()
    flash('Your appointment has been cleared!', 'success')
    return redirect(url_for('homeDoc'))

@app.route("/verify")
def verify():
    
    newdata=dataset.append(array)
    flash('This user check has been added to the dataset.', 'success')
    return redirect(url_for('servicesDoc'))
