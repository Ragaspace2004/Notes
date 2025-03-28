# all authentication routes will be written here

from flask import Blueprint, render_template, request, flash,url_for,redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user=User.query.filter_by(email=email).first()
    if user:
      if(user.password == password):
        flash('Login successful', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Invalid password,Try again', category='error')
    else:
      flash('Email does not exist', category='error')
  return render_template('login.html', user=current_user)
    
    
@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))
    
@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    firstName = request.form.get('firstName')
    password = request.form.get('password')
    password2= request.form.get('password2')
    
    # check if email already exists
    user = User.query.filter_by(email=email).first()
    if user:
      flash('Email already exists',category='error')
    # check if passwords match
    elif(len(email)<4):
      flash('Email must be greater than 3 characters',category='error')
    elif(len(firstName)<2):
      flash('First name must be greater than 1 character',category='error')
    elif(len(password)<7):
      flash('Password must be at least 7 characters',category='error')
    elif password != password2:
      flash('Passwords do not match',category='error')
    else:
      new_user = User(email=email, first_name=firstName, password=password)
      db.session.add(new_user)
      db.session.commit()
      flash('Registration successful',category='success')
      login_user(new_user,remember=True)
      return redirect(url_for('views.home'))
  return render_template('signup.html', user=current_user)
  