from flask import Blueprint, render_template, request, redirect, url_for, flash


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')