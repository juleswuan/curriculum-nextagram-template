from flask import Blueprint, jsonify
from models.image import Image

images_api_blueprint = Blueprint('images_api',
                             __name__,
                             template_folder='templates')

@images_api_blueprint.route('/', methods=['GET'])
def index():
    # get all images
    # construct the dict that represents an image
    # return all the dicts to a list
    # convert the list into a JSON

    images = [
        image.image_url for image in Image.select()
    ]

    return jsonify(images)
