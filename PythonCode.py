from flask import Flask, render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt, check_password_hash
from flask_wtf.csrf import CSRFProtect
import pymysql.cursors
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from Forms import Register, Volunteer, LoginForm

connection = pymysql.connect('localhost',
                             'root',
                             'Nikketan',
                             'COMEIT',
                             # Fetch Results as Python Dictionary, Easier to access specific columns
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
app = Flask(__name__)

# How to generate Secret Key :
"""
Open terminal, type python or py and then type the following code.
    import uuid
    uuid.uuid4()
Paste the String Generated.
"""

# Secret Key For Configurations
app.config['SECRET_KEY'] = 'c4ceadd4-4e99-475d-9a27-f23b7f219f52'
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)


class User(UserMixin):
    # Boilter Plate for User Management
    pass


@login_manager.user_loader
def load_user(user_name):
    # Returns a User Object based on user_id (user_name in this case)
    cursor.execute(
        'SELECT * FROM VOLUNTEERS WHERE NAME = \'%s\'' % user_name)
    row = cursor.fetchone()

    if row:
        # if user exists in the database
        user = User()
        user.id = row.get('NAME')
        user.name = row.get('NAME')
        user.contact = row.get('CONTACT')
        user.job = row.get('JOB')
        return user
    else:
        # if user doesn't exist, return None
        return


@login_manager.unauthorized_handler
def unauthorized_handler():
    # What to do when the user is not logged in
    flash('You need to be Logged in to view that page', 'danger')
    return redirect(url_for('Login'))


@app.route('/')
@app.route('/Home')
def Homepage():
    return render_template('Homepage.html', loggedIn=current_user.is_authenticated)


@app.route('/About')
def About():
    return render_template('About.html', loggedIn=current_user.is_authenticated)


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
        cursor.execute('INSERT INTO REGISTER VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
            Name, Email, College, Event, Group, Contact, Volunteer))
        connection.commit()
        return redirect(url_for('Homepage'))
    return render_template("Register.html", form=form)


@app.route("/MemberRegister", methods=['GET', 'POST'])
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
        Phones_l = [element for tupl in Phones for element in tupl]
        if Contact in Phones_l:
            flash(f'The Contact Number is Already Registered.', 'danger')
            return redirect(url_for('Volunteer1'))
        if Job == '1':
            Job = "Call and Confirm"
        elif Job == '2':
            Job = "Crowd Management"
        elif Job == '3':
            Job = "Information Center"
        elif Job == '4':
            Job = "Event Management"
        elif Job == '5':
            Job = "Ceremonial Duties"
        flash(f'Registered As A Volunteer. Congrats', 'success')
        cursor.execute('INSERT INTO VOLUNTEERS VALUES(\'%s\',\'%s\',\'%s\',\'%s\')' % (
            Name, hashed_pass, Job, Contact))
        connection.commit()
        return redirect(url_for('Homepage'))
    return render_template('VolunteerRegister.html', form=form)


@app.route('/Login', methods=['GET', 'POST'])
def Login():
    # If user is already signed in, redirect to Accounts page
    if (current_user.is_authenticated):
        return redirect(url_for('account'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            cursor.execute(
                'SELECT * FROM VOLUNTEERS WHERE NAME = \'%s\'' % form.Name.data)
            row = cursor.fetchone()
            if row:
                # User Exists
                # Retrieves the User's hashed password from DB
                password = row.get('PASSWORD')
                if check_password_hash(password, form.Password.data):
                    # Creates a new User object and assigns the name as it's ID
                    user = User()
                    user.id = row.get('NAME')

                    # Logs the user object in.
                    login_user(user)
                    flash("You've Successfully Logged In Into Your Account.", 'success')
                    return redirect(url_for('Homepage'))
                else:
                    flash(f'Incorrect Password Entry.', 'danger')
                    return redirect(url_for('Login'))
            else:
                flash(f'The Name is Not Registered.', 'danger')
                return redirect(url_for('Login'))
        return render_template('Login.html', form=form)


@app.route('/account')
# Login required states that user has to be logged in to view this page
@login_required
def account():
    currentUser = {
        'id': current_user.id,
        'name': current_user.name,
        'contact': current_user.contact,
        'job': current_user.job
    }
    return render_template('Account.html', user=currentUser)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('Login'))


if __name__ == '__main__':
    app.run(debug=True)
