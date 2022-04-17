from pymongo import MongoClient
import hashlib
import itertools

# MongoDB Connection #
cluster = MongoClient("mongodb+srv://abbask31:aggletes.tech@cluster0.8dwgr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Agletes"]
collection = db["users"]

# Ticket Class #
class Ticket:
    id_iter = itertools.count()
    def __init__(self, email, eventid, date, sport, location, checked_in = False):

        self.email      = email
        self.eventid    = eventid
        self.date       = date
        self.sport      = sport
        self.location   = location
        self.checked_in = checked_in

        self.tid = email + eventid

def hash_password(password):
    crypt = hashlib.sha512()
    crypt.update(password.encode('utf-8'))
    return crypt.hexdigest()

def sign_up(name, email, year, number, password):
    
    post = { 
        "_id"       : email,
        "tickets"   : [],
        "password"  : password,
        "extras"    : {
            "name"          : name,
            "year"          : year,
            "phone_number"  : number
        }
    }
    collection.insert_one(post)

def add_ticket(ucd_email, ticket):
    collection.update_one({"_id":ucd_email}, {"$push": {"tickets":ticket.__dict__}})

def remove_ticket(ucd_email, ticket):
    collection.update_one({"_id":ucd_email}, {"$pull": {"tickets":{"tid":ticket.tid}}})

def update_check_in(ucd_email, ticket):
    collection.update_one({"_id":ucd_email, "tickets.tid": ticket.tid}, {"$set": {"tickets.$.checked_in":True}})

def delete_user(ucd_email):
    collection.update_one({"_id":ucd_email})

def delete_db():
    collection.delete_many({})

def log_in(ucd_email, password):
    user = collection.find_one({"_id":ucd_email})
    if user is None:
        return "This account has not been registered. Please try again or Create an Account"
    else:
        if password == user["password"]:
            return user
        elif hash_password(password) != user["password"]:
            return "Incorrect Password"

def ticket_status(ucd_email, ticket):
    user = collection.find_one({"_id":ucd_email})

    return user["tickets"][ticket.id]["checked_in"]