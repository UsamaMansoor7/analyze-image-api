from flask import Blueprint, request, jsonify
from ..extensions import openai
from ..utils.image_analyzer_utils import encode_image, allowed_file

import base64
import requests

analyzer_bp = Blueprint("image_analyzer", __name__)


@analyzer_bp.route('/analyze-image', methods=['POST'])
def analyze_image():
    try:
        image_file = request.files['image']

        if image_file and allowed_file(image_file.filename):
            
            base64_image = encode_image(image_file)

            headers = {
                "Content-Type": "application/json", 
                "Authorization": f"Bearer {openai.api_key}"
            }

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What’s in this image?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                description = result['choices'][0]['message']['content']
                return jsonify({'description': description})
            else:
                return jsonify({'error': f"OpenAI API request failed with status code {response.status_code}"}), 500
        else:
            return jsonify({'error': 'Invalid or not allowed file'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

