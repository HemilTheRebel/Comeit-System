from flask import Flask, render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt, check_password_hash
from flask_wtf.csrf import CSRFProtect
import pymysql.cursors

from FlaskCode.PythonCodes.Forms import Register, Volunteer, LoginForm

connection = pymysql.connect('localhost', 'root', 'sarveshsj25', 'COMEIT')
cursor = connection.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Shady45'  # Secret Key For Configurations
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)


@app.route('/')
@app.route('/Home')
def Homepage():
    return render_template('Homepage.html')


@app.route('/About')
def About():
    return render_template('About.html')


@app.route('/Register', methods=['GET', 'POST'])
def Register1():
    form = Register(request.form)
    if form.validate_on_submit():
        Name = form.Name.data
        Email = form.Email.data
        College = form.College.data
        if form.Events.data == '1':
            Event = "Frontliners of FrontEnd"
        elif form.Events.data == '2':
            Event = "Battles of BackEnd"
        elif form.Events.data == '3':
            Event = "Hackathon"
        elif form.Events.data == '4':
            Event = "Tour-de-GPP"
        elif form.Events.data == '5':
            Event = "Flash"
        Group = form.Group.data
        Contact = form.Phone.data
        Volunteer = form.Volunteer.data
        cursor.execute('INSERT INTO REGISTER VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' %(Name,Email,College,Event,Group,Contact,Volunteer))
        connection.commit()
        return redirect(url_for('Homepage'))
    return render_template("Register.html", form=form)


@app.route("/MemberRegister",methods=['GET','POST'])
def Volunteer1():
    form = Volunteer()
    if form.validate_on_submit():
        Name = form.Name.data
        Password = form.Password.data
        hashed_pass = bcrypt.generate_password_hash(Password).decode('utf-8')
        Job = form.Job.data
        Contact = form.Contact.data
        cursor.execute('SELECT CONTACT FROM VOLUNTEERS ;')
        Phones = cursor.fetchall()
        Phones_l =[element for tupl in Phones for element in tupl]
        if Contact in Phones_l:
            flash(f'The Contact Number is Already Registered.','danger')
            return redirect(url_for('Volunteer1'))
        if Job == '1' :
            Job = "Call and Confirm"
        elif Job == '2':
            Job = "Crowd Management"
        elif Job == '3':
            Job = "Information Center"
        elif Job == '4':
            Job = "Event Management"
        elif Job == '5':
            Job = "Ceremonial Duties"
        flash(f'Registered As A Volunteer. Congrats','success')
        cursor.execute('INSERT INTO VOLUNTEERS VALUES(\'%s\',\'%s\',\'%s\',\'%s\')' %(Name,hashed_pass,Job,Contact))
        connection.commit()
        return redirect(url_for('Homepage'))
    return render_template('VolunteerRegister.html',form = form)


@app.route('/Login',methods = ['GET','POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor.execute('SELECT NAME FROM VOLUNTEERS')
        Names = cursor.fetchall()
        Name =  [element for tupl in Names for element in tupl]
        if form.Name.data in Name :
            cursor.execute('SELECT PASSWORD FROM VOLUNTEERS WHERE NAME = \'%s\'' % form.Name.data)
            passwords = cursor.fetchall()
            password = [element for tupl in passwords for element in tupl]
            if check_password_hash(password[0], form.Password.data):
                flash(f"You've Successfully Logged In Into Your Account.", 'success')
                return redirect(url_for('Homepage'))
            else :
                flash(f'Incorrect Password Entry.','danger')
                return redirect(url_for('Login'))
        else :
            flash(f'The Name is Not Registered.','danger')
            return redirect(url_for('Login'))
    return render_template('Login.html',form = form)


if __name__ == '__main__':
    app.run(debug=True)
