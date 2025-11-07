import db
import datetime as dt
from flask import Flask,render_template, request, url_for, flash, redirect, session
from flask_cors import CORS
from models.users import login_manager, User, login_user, login_required
from models.forms import RegisterForm, LoginForm, CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = db.SESSION_SECRET_KEY

csrf = CSRFProtect(app)
CORS(app)

#session secret key


#Set up Flask Login
login_manager.init_app(app)
login_manager.login_view ='view'



@login_manager.user_loader # imported login_manager from the forms.py
def load_user(user_id):
    user_data = User.objects({'_id': user_id}).first()
    if user_data:
        return(User(user_data))
    return 



@app.route("/home")
def homes():
    return render_template("home.html") # renders the homepage


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm() # creates an instance of the loginform class
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()  #checks for is any email is found in the database that matches the one provided by the user
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in Successfully", 'success')
            return redirect(url_for("/index"))
        
        else:
            return flash("Invalid Email or Password. Try again!", 'warning')
    return render_template('login.html', form=form)


#Register route
@app.route("/signup", methods=["GET", "POST"])
def register():
    form = RegisterForm() # calls the Register WTForm from forms.py file
    if form.validate_on_submit():
        existing_user = User.objects({'email':form.email.data}).first() # checks if the email already exist in the database

        if existing_user:
            flash("Email already Registered. Please Login or try another email", 'warning') # shows an alert fo successfully registering!
            return redirect(url_for("register"))
        
        hash_password = generate_password_hash(form.password.data) # hashes the password of the user
        users = User(username=form.username.data,
                      email=form.email.data,
                        password=hash_password)
        
        users.save() # stores the provided data to the database

        flash("Registration Successful, Plese Login")
        return redirect(url_for('login')) # redirects the the Login page!
   
    return render_template('register.html', form=form)







today = dt.datetime.today()
# gets the data of every registered user including name and date of birth etc.

# This is the home page route to to show the active Birthdays 
@login_required
@app.route('/index',methods=["GET", "POST"])
def home():
    saved_birthdays= db.DateOfBirth.objects().all()

    todays_birthday = []
    
    for i in saved_birthdays:

        if i["Day"] == today.day and i["Month"] == today.month:
            Bday = f"Today is {i['Surname']} {i['FirstName']}'s Birthday."
            age = f"They are {today.year - i["Year"]}"
            
            todays_birthday.append({"Bday":Bday, "age":age})
            
    if not todays_birthday:
        todays_birthday.append({"Bday": "There are no Birthdays Today!!", "age": ""})

    message = None
    if request.method == "POST" and len(request.form) > 0:   
        firstname = request.form['firstname']
        surname = request.form['surname']
        day = request.form['day']
        month = request.form['month']
        year = request.form['year']
        phone = request.form['phone']
        notes = request.form['notes']


        # creating a new entry/document for the database
        new_dob = db.DateOfBirth(
            Firstname =firstname,
            Surname = surname,
            Day = day,
            Month = month,
            Year = year,
            Phone = phone,
            Notes = notes
        )
        #saving the data to the database
        new_dob.save()
        message = f"Saved {firstname} {surname}'s Birthday data" 

    return render_template('index.html', birthdays = todays_birthday, message = message, url_for=url_for)


#this is the route that the javascript fetch function listens to, to post the form data to the database
@login_required
@app.route('/submit',methods=[ "POST"])
def submit():
     if len(request.form) > 0:   
        if request.method == "POST":
            firstName = request.form['firstname']
            surname = request.form['surname']
            day = request.form['day']
            month = request.form['month']
            year = request.form['year']
            phone = request.form['phone']
            notes = request.form['notes']


            # creating a new entry/document for the database
            new_dob = db.DateOfBirth(
                FirstName =firstName,
                Surname = surname,
                Day = day,
                Month = month,
                Year = year,
                Phone = phone,
                Notes = notes
            )
            #saving the data to the database
            new_dob.save()
            return "Successfully added" ,201
    


# if __name__ == '__main__':
#     app.run(debug=True)