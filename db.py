from mongoengine import StringField, IntField, Document, connect, DateTimeField
from os import getenv
from dotenv import load_dotenv
load_dotenv()
DB_URI = getenv("DB_URI")

SESSION_SECRET_KEY = getenv('SESSION_SECRET_KEY')


#connecting to the DB
connect("dob_DB", host=DB_URI)

print("successfully connected to The Database", 200)

#creating the fields in mongodb to store the data gotten from the FE
class DateOfBirth(Document):
    Surname = StringField(required=True)
    FirstName = StringField(required=True)
    Day = IntField(required=True, max_value=31)
    Month = IntField(required=True, max_value=12)
    Year = IntField(required=True, min_value=1940)
    Phone = IntField(max_length = 13)
    Notes = StringField(max_length=200)


    def to_db (self):
        return{
        "Surname": self.Surname,
        "FirstName": self.FirstName,
        "Day": self.Day,
        "Month": self.Month,
        "Year": self.Year,
        "Phone": self.Phone,
        "Notes":self.Notes
        }