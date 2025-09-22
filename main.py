import datetime as dt
from flask import Flask,render_template, request, url_for
from flask_cors import CORS
import db


app = Flask(__name__)
CORS(app)

today = dt.datetime.today()
# gets the data of every registered user including name and date of birth etc.



# This is the home page route to to show the active Birthdays 
@app.route('/',methods=["GET", "POST"])
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