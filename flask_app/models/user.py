from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from datetime import date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name=data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.sends=0
        self.messages=[]

#CREATE
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO users 
        ( first_name , last_name , email, password) 
        VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s );"""
        return connectToMySQL('private_wall_schema').query_db( query, data )



#READ
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        result= connectToMySQL('private_wall_schema').query_db(query)
        users=[]
        for user in result:
            users.append(cls(user))
        return users
    @classmethod
    def lastIndex(cls):
        query="SELECT * FROM users WHERE id=(SELECT max(id) FROM users);"
        user=(connectToMySQL('private_wall_schema').query_db(query))[0]
        return user




#UPDATE
    @classmethod
    def update(cls, data):
        query = """
        UPDATE users 
        SET email = %(email)s, 
        first_name=%(first_name)s, 
        last_name=%(last_name)s 
        WHERE id = %(id)s;"""
        return connectToMySQL('private_wall_schema').query_db( query, data )





#DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = (%(id)s);"
        return connectToMySQL('private_wall_schema').query_db(query, data)




#static
    @staticmethod
    def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        for email in User.get_all():
            if user['email']== email.email:
                flash("This email is taken")
                is_valid= False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("last name must be at least 2 characters.")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be at least 8 characters.")
            is_valid = False
        if user['password']!= user['password_confirm']:
            flash("passwords don't match")
            is_valid=False
        if   re.search('[A-Z]',user['password']) is None:
            flash("Password must contain at least one capital letter and one number.")
            is_valid=False
        elif re.search('[0-9]',user['password']) is None:
            flash("Password must contain at least one capital letter and one number.")
            is_valid=False 
        elif re.search('[a-z]',user['password']) is None: 
            flash("Password must contain at least one capital letter and one number.")
            is_valid=False          
        # print(user['birthday'])
        # birthday=datetime.strptime(user['birthday'],"%Y-%m-%d")
        # print(birthday.year)
        # age=calculate_age(birthday)
        # print (age)
        # if age<16:
        #     flash("you are too young to use this site")
        #     is_valid=False
        return is_valid
def calculate_age(born):
    today = date.today()
    age=today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    print(age)
    return age