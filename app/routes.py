from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    context = {
        'form': form
    }
    if form.validate_on_submit():  # redirect to index after successful submission
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email and/or password. Try again.")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!")  # flash a success message
        # redirect to index page after message is displayed
        return redirect(url_for('index'))
    return render_template('login.htm', **context)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    context = {
        'register_form': register_form
    }
    if register_form.validate_on_submit():
        u = User(name=register_form.name.data, email=register_form.email.data)
        u.set_password(register_form.password.data)
        db.session.add(u)
        db.session.commit()
        flash("You have sucessfully registered!")
        return redirect(url_for('login'))
    return render_template('register.htm', **context)
    
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))
