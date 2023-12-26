from flask import Blueprint

analyzer_bp = Blueprint("analyzer", __name__)

from . import image_analyzer  # noqa
