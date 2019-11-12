from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/', methods=['GET'])
def new():
    return render_template('sign-in.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    # get username/email (unique) + password
    username = request.form.get('username')
    password = request.form.get('password')
    # check user exists
    user = User.get_or_none(username=username)
    if user:
        # check password match
        match = check_password_hash(user.password, password)

        if match:
            #login user           
            flash("It's a match")
            return redirect(url_for('create'))
        else:
            flash('Wrong password')
            return render_template('sign-in.html')
    else:
        flash('No user found')
        return render_template('sign-in.html')