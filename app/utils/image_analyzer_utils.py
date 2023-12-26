
import base64
def encode_image(image):
    if isinstance(image, str):  # If an image path is provided
        with open(image, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    elif hasattr(image, 'read'):  # If image content is directly passed
        return base64.b64encode(image.read()).decode('utf-8')
    else:
        raise ValueError("Invalid image format")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}
