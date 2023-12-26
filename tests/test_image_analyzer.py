import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.utils.image_analyzer_utils import encode_image, allowed_file
from app.api.image_analyzer import analyzer_bp


class ImageAnalyzerTests(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(analyzer_bp)
        self.client = self.app.test_client()

    def test_allowed_file_valid_extension(self):
        valid_filename = "image.jpg"
        result = allowed_file(valid_filename)
        self.assertTrue(result)

    def test_allowed_file_invalid_extension(self):
        invalid_filename = "image.txt"
        result = allowed_file(invalid_filename)
        self.assertFalse(result)

    def test_allowed_file_no_extension(self):
        no_extension_filename = "image"
        result = allowed_file(no_extension_filename)
        self.assertFalse(result)

    @patch('requests.post')
    def test_analyze_image_success(self, mock_post):
        mock_post.return_value.status_code = 500  # Simulating a 400 Bad Request error
        mock_post.return_value.json.return_value = {'error': '400 Bad Request: The browser (or proxy) sent a request that this server could not understand.'}
        response = self.client.post('/analyze-image', data={'image': 'ABC.jpeg'})
        data = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)

    @patch('requests.post')
    def test_analyze_image_openai_error(self, mock_post):
        mock_post.return_value.status_code = 500
        response = self.client.post('/analyze-image', data={'image': 'XYZ.jpeg'})
        data = response.get_json()
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
