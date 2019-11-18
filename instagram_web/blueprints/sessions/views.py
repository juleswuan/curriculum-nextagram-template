from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, login_user, logout_user
from models.user import User
from werkzeug.security import check_password_hash
from instagram_web.util.google_oauth import oauth


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
            return redirect(url_for('users.index')) # redirect to homepage 
        else:
            flash('Wrong password', 'danger')
            return render_template('sign-in.html')
    else:
        flash('No user found', 'danger')
        return render_template('sign-in.html')

# google login (sends to google)
@sessions_blueprint.route('/login/google', methods=['GET'])
def google_login():
    redirect_url = url_for('sessions.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_url)

# allows login (returns from google)
@sessions_blueprint.route('/authorize/google', methods=['GET'])
def authorize_google():
    token = oauth.google.authorize_access_token()
    if not token:
        flash('error - token', 'danger')
        return render_template('sign-in.html')
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    # check if user exists in db
    user = User.get_or_none(User.email == email)
    if not user:
        flash ('error - user', 'danger')
        return render_template('sign-in.html')
    else:
        flash('Welcome')
        login_user(user)
        return redirect(url_for('users.index'))

# sign out current user
@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    flash ('Successfully signed out', 'success')
    return redirect(url_for('sessions.new'))