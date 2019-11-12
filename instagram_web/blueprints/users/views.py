from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():

    username = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(username=username, email=email, password=password) 

    if user.save():
        print(user.username)
        flash('New user has been added!')
        return redirect(url_for('users.new')) 
    else: 
        print(user.errors)
        for error in user.errors:
            flash(error)
        return render_template ('users/new.html', username=username, email=email, password=password)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    # get username
    # check that it matches authenticated login user
    # pass username to template
    return render_template('users/profile.html', username=username)


@users_blueprint.route('/', methods=["GET"])
def index():
    # homepage
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User[id]
    if current_user.is_authenticated and current_user.id == user.id:
        return render_template('users/edit.html', user=user)
    else: 
        flash(f"Not allowed to update {user.username}'s profile")
        return render_template('users/edit.html', user=current_user)


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User[id]
    if current_user == user:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        if user.save():
            flash('Successfully updated!')
            return redirect (url_for('users.edit', id=id))
        else: 
            flash('Unable to update profile')
            return render_template('users/edit.html', user=user)
    else:
        flash(f"Not allowed to update {user.username}'s profile'")
        return render_template('users/edit.html', user=user)

