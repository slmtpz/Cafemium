from cafemiummongo import db, ObjectId


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
            self.firmName = user_doc['firmName']
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


def check_phone(phone):
    result = db.users.find_one({'phone': phone})
    if result is None:
        return 1
    else:
        return 0


def add_user(user_type, firm_name, name, email, phone, hashed_password):
    db.users.insert_one({
        'type': user_type,
        'firmName': firm_name,
        'name': name,
        'email': email,
        'phone': phone,
        'password': hashed_password
    })
