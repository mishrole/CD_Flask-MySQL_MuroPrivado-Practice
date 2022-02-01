from bcrypt_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from datetime import datetime

TEXT_REGEX = re.compile(r'^[A-Za-z\u00C0-\u017F\.\-\s]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[A-Z])[a-zA-Z\d]{8,}$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.birthday = data['birthday']
        self.gender = data['gender']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.isBlocked = data['isBlocked']
        self.messages = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users where isBlocked like 0 order by firstname asc;"
        results = connectToMySQL('private_wall_schema').query_db(query)

        users = []

        if results:
            if len(results) > 0:
                for user in results:
                    users.append(cls(user))

        return users

    @classmethod
    def get_all_exclude_current(cls, data):
        query = "SELECT * FROM users where id not like %(userId)s and isBlocked like 0 order by firstname asc;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        users = []

        if results:
            if len(results) > 0:
                for user in results:
                    users.append(cls(user))

        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (firstname, lastname, birthday, gender, email, password, created_at, updated_at) VALUES (%(firstname)s, %(lastname)s, %(birthday)s, %(gender)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('private_wall_schema').query_db(query, data)

    @classmethod
    def findUserByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        user = None

        if results:
            if len(results) > 0:
                user = cls(results[0])

        return user

    @classmethod
    def findUserById(cls, data):
        query = "SELECT * FROM users WHERE id = %(userId)s;"
        results = connectToMySQL('private_wall_schema').query_db(query, data)

        user = None

        if results:
            if len(results) > 0:
                user = cls(results[0])

        return user

    @classmethod
    def blockUser(cls, data):
        query = "UPDATE users SET isBlocked = 1, updated_at = NOW() WHERE users.id = %(userId)s"
        return connectToMySQL('private_wall_schema').query_db(query, data)

    # @classmethod
    # def delete(cls, data):
    #     query = "DELETE FROM users WHERE id = %(userId)s"
    #     return connectToMySQL('private_wall_schema').query_db(query, data)

    @staticmethod
    def validateRegister(user):
        is_valid = True

        email = user['email']
        password = user['password']
        firstname = user['firstname']
        lastname = user['lastname']
        birthday = user['birthday']
        gender = user['gender']
        
        if gender == 'Self describe':
            gender = user['other']

        if len(birthday) == 0:
            flash('Birthday must be selected.', 'register_error')
            is_valid = False
        else:
            today = datetime.now()
            birthdayConverted = datetime.strptime(birthday, "%Y-%m-%d")
    
            if birthdayConverted > today:
                flash('Birthday must be a date in the past', 'register_error')
                is_valid = False

        if len(firstname) < 2:
            flash('First name must be at least 2 characters long', 'register_error')
            is_valid = False

        if len(lastname) < 2:
            flash('Last name must be at least 2 characters long', 'register_error')
            is_valid = False

        if not TEXT_REGEX.match(firstname):
            flash('First name must only contain letters and . -', 'register_error')
            is_valid = False

        if not TEXT_REGEX.match(lastname):
            flash('Last name must must only contain letters and . -', 'register_error')
            is_valid = False

        if len(gender) == 0:
            flash('Select an option or self describe', 'register_error')
            is_valid = False

        if not TEXT_REGEX.match(gender):
            flash('Gender must only contain letters and . -', 'register_error')
            is_valid = False

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'register_error')
            is_valid = False

        if not PASSWORD_REGEX.match(password):
            flash('Password must be at least 8 characters long and contain 1 uppercase letter and 1 number without special characters', 'register_error')
            is_valid = False

        if user['password'] != user['password_confirmation']:
            flash('Password and confirmation do not match!', 'register_error')
            is_valid = False
        
        if User.findUserByEmail({'email': email}) != None:
            flash('Email address is already taken!', 'register_error')
            is_valid = False

        return is_valid

    @staticmethod
    def validateLogin(user):
        is_valid = True

        email = user['email']

        if not EMAIL_REGEX.match(email):
            flash('Invalid email address!', 'login_error')
            is_valid = False

        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long', 'login_error')
            is_valid = False

        if User.findUserByEmail({'email': email}) == None:
            flash('Invalid Email / Password', 'login_error')
            is_valid = False
        else:
            if User.findUserByEmail({'email': email}):
                findUser = User.findUserByEmail({'email': email})

                if(findUser.isBlocked == True):
                    flash('Your account is blocked!', 'login_error')
                    is_valid = False     

        return is_valid