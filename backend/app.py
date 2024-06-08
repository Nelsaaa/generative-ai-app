from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

openai.api_key = app.config['OPENAI_API_KEY']

@app.route('/')
def home():
    return "Welcome to the AI Generative Application!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')

    try:
        # Génération de texte
        text_response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150
        )
        text = text_response.choices[0].text.strip()

        # Limiter le texte à 4 lignes
        lines = text.split('\n')
        limited_text = '\n'.join(lines[:4])

        # Génération d'image en utilisant le texte généré
        image_response = openai.Image.create(
            prompt=limited_text,
            n=1,
            size="1024x1024"
        )
        image_url = image_response.data[0].url

        return jsonify({'text': limited_text, 'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
