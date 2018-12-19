from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    # has to be an integer, stored in a column, primary_key identifies uniqueness and auto-increments among all users/mandatory field
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))  # validates name is less than 50 chars
    # validates email is less than 120 chars
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password)  # setting our input to hashed password

    def check_password(self, password):
        # comparing our input to hashed password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User: {self.name} | {self.email}>"

    #keeps track of users as they jump from page to page
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))
