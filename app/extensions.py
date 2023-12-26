from flask import Flask

class OpenAI:
    def init_app(self, app: Flask):
        self.api_key = app.config.get("OPENAI_API_KEY", None)

openai = OpenAI()
