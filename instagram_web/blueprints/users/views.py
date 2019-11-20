from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.image import Image
from models.user import User
from models.follow import Follow
from werkzeug.security import generate_password_hash 
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from config import Config


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

# Sign up new user
@users_blueprint.route('/', methods=['POST'])
def create():

    username = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(username=username, email=email, password=password) 

    if user.save():
        print(user.username)
        flash('New user has been added!', 'success')
        return redirect(url_for('users.new')) 
    else: 
        print(user.errors)
        for error in user.errors:
            flash(error, 'danger')
        return render_template ('users/new.html', username=username, email=email, password=password)


# user profile page
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.select().where(User.username == username).get()
    # code to check if user is an idol who has approved me (fan)
    return render_template('users/profile.html', user=user)


# homepage / all users feed
@users_blueprint.route('/', methods=["GET"])
@login_required
def index():
    users = User.select()
    images = Image.select().where(Image.user << users)
    return render_template('home.html', users=users, images=images)


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User[id]
    if current_user.is_authenticated and current_user.id == user.id:
        return render_template('users/edit.html', user=user)
    else: 
        flash(f"Not allowed to update {user.username}'s profile", 'danger')
        return render_template('users/edit.html', user=current_user)

# upload profile image
@users_blueprint.route('/profile/<id>', methods=['POST'])
@login_required
def update_profile_img(id):
	# get a file from request
    file = request.files['user_file']
	# if no file in request (user submit on empty form)
    if not file:
        flash("Please select a file", 'danger')
        return render_template('users/edit.html')
	# if there is a file in request & is allowed type
    elif file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)
        if not output:
            flash(f'Unable to upload {file.filename}', 'danger')
            return render_template('users/edit.html')
        else:
            # get current user
            # save profile image link 
            user = User.update(profile_image = output).where(User.id == current_user.id)
            user.execute()
            flash(f'Successfully uploaded {file.filename}', 'success')
            return redirect(url_for('users.show', username=current_user.username))
        

# update user details
@users_blueprint.route('/update/<id>', methods=['POST'])
@login_required
def update(id):
    user = User[id]
    if current_user == user:
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        if user.save():
            flash('Successfully updated!', 'success')
            return redirect (url_for('users.edit', id=id))
        else: 
            flash('Unable to update profile', 'danger')
            return render_template('users/edit.html', user=user)
    else:
        flash(f"Not allowed to update {user.username}'s profile", 'danger')
        return render_template('users/edit.html', user=user)


# make account private
@users_blueprint.route('/private/<id>', methods=['POST'])
@login_required
def make_private(id):
    user = User[id]
    if current_user == user:
        user.is_private = True
        if user.save():
            flash ('Account setting updated', 'success')
            return redirect (url_for('users.edit', id=id))
        else:
            flash('Unable to update account setting', 'danger')
            return render_template('users/edit.html', user=user)
    else:
        flash(f"Not allowed to change {user.username}'s account setting", 'danger')
        return render_template('users/edit.html', user=user)


# follow user
@users_blueprint.route('/follow/<username>', methods=["POST"])
@login_required
def follow(username):
    idol_id = request.form.get('idol_id')
    f = Follow(fan=current_user.id, idol=idol_id)
    idol = User.get_by_id(idol_id)
    f.save()
    flash(f'You are now following {idol.username}', 'success')
    return redirect (url_for('users.show', username=idol.username))


