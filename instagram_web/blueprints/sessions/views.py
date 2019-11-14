from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/', methods=['GET'])
def new():
    return render_template('sign-in.html')

# sign in user
@sessions_blueprint.route('/', methods=['POST'])
def create():
    # get email (unique) + password
    email = request.form.get('email')
    password = request.form.get('password')
    # check user exists
    user = User.get_or_none(email=email)
    if user:
        # check password match
        match = check_password_hash(user.password, password)

        if match:
            #login user 
            # session['user_id'] = user.id 
            login_user(user)    
            flash("Successfully signed in", 'success')
            return redirect(url_for('users.index')) # should redirect to homepage 
        else:
            flash('Wrong password', 'danger')
            return render_template('sign-in.html')
    else:
        flash('No user found', 'danger')
        return render_template('sign-in.html')

# sign out current user
@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    flash ('Successfully signed out', 'success')
    return redirect(url_for('sessions.new'))