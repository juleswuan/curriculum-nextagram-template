from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    username = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.CharField(null=False)

    def validate(self):
        # check username constraints
        duplicate_username = User.get_or_none(User.username == self.username)

        if duplicate_username:
            self.errors.append('Username not unique')
        elif len(self.username) < 6 or len(self.username) > 20:
            self.errors.append('Username must be between 6 and 20 chars')
        elif not re.match(r"^[a-zA-Z0-9_.-]+$", self.username):
            self.errors.append('Username must contain ONLY alphanumeric chars (a-z, A-Z, 0-9) and underscore / dot / dash symbols (_ . -)')

        # check email constraints
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_email:
            self.errors.append('Email is already in use. Please enter another email')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.errors.append('Email not in correct format')

        # check password constraints
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$" , self.password):
            self.errors.append('Password must be min. 8 chars, and contain min. one letter, one number and one special character')
        else:
            self.password = generate_password_hash(self.password)
        