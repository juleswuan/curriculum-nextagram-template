from flask import Blueprint, jsonify
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    # get all users
    # construct the dict that represents a user
    # return all the dicts to a list
    # convert the list into a JSON

    users = User.select()
    all_users = []
    for user in users:
        user = {"id": user.id, "username": user.username, "profileImage": user.profile_image_url}
        all_users.append(user)

    return jsonify(all_users), 201