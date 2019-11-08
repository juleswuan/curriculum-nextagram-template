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
    # user = User(**request.form.to_dict())
    # if user.save():
    #     print(user.username, user.email, user.password)

    password = request.form.get('password')
    hashed = generate_password_hash(password)

    username = request.form.get('name')
    if username.match("^[a-zA-Z0-9_.-]+$", username) and len(username) >= 8:
        user = User(username=username, email=request.form.get(
            'email'), password=hashed)
        if user.save(): # ok to save to db
            flash('New user has been added!')
            return redirect(url_for('users.new'))
        else:
            return render_template ('users/new.html')
    else:
        flash('Invalid username.\nPlease choose a username that is: \nmin. 8 chars in length\ncontains only alphanumeric chars (a-z, A-Z, 0-9) and (_ . -)')
        return render_template ('users/new.html')


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
