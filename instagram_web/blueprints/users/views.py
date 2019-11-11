from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
