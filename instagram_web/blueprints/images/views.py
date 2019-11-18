from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from models.user import User
from models.image import Image


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('new.html')

# upload image
@images_blueprint.route('/', methods=['POST'])
@login_required
def create():
    file = request.files['image_file']
    if not file:
        flash("Please select a file", 'danger')
        return render_template('images/new.html')
    elif file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)
        if not output:
            flash(f'Unable to upload {file.filename}', 'danger')
            return render_template('users/edit.html')

        else:
            user = User.get_by_id(current_user.id)
            image = Image(image_path=output, user=user)
            image.save()
            flash(f'Successfully uploaded {file.filename}', 'success')
            return redirect(url_for('users.show', username=user.username))

# delete image
@images_blueprint.route('/<id>/delete', methods=['POST'])
@login_required
def delete(id):
    image = Image.get_by_id(id)
    image.delete_instance()
    return redirect(url_for('images.show'))

# display a specific user's images
@images_blueprint.route('/<id>', methods=['GET'])
@login_required
def show(id):
    user = User[current_user.id]
    return render_template('users/profile.html', user=user)