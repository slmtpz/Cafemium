from cafemiummongo import db, ObjectId
from constants import roles


class User:
    def __init__(self, user_email):
        user_doc = get_user(user_email)
        if user_doc is None:
            self.email_invalid = True
            self.is_authenticated = False
            self.is_active = False
            self.is_anonymous = True
        else:
            self.email_invalid = False
            self.type = user_doc['type']
            self.firm_name = user_doc['firm_name']
            self.name = user_doc['name']
            self.email = user_doc['email']
            self.phone = user_doc['phone']
            self.password = user_doc['password']

            self.is_authenticated = True
            self.is_active = True
            self.is_anonymous = False

    def get_id(self):
        return self.email


def get_user(user_email):
    return db.users.find_one({'email': user_email})


def check_email(email):
    result = db.users.find_one({'email': email})
    if result is None:
        return 1
    else:
        return 0


def add_user(user_type, firm_name, name, email, phone, hashed_password):
    db.users.insert_one({
        'type': roles[user_type],
        'firm_name': firm_name,
        'name': name,
        'email': email,
        'phone': phone,
        'password': hashed_password
    })
