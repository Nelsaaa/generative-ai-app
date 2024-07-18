from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import uuid
import json
from sqlalchemy import create_engine, Column, String, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Charger la clé secrète depuis le fichier .env
secret_key = os.getenv('SECRET_KEY')
if not secret_key:
    raise ValueError("No SECRET_KEY set for Flask application")
app.secret_key = secret_key

openai.api_key = os.getenv('OPENAI_API_KEY')

# Configuration de la base de données
DATABASE_URL = "sqlite:///sessions.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ChatSession(Base):
    __tablename__ = 'sessions'
    session_id = Column(String, primary_key=True, index=True)
    messages = Column(Text, nullable=False)
    theme = Column(String, nullable=True)
    num_characters = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    era = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    ending_type = Column(String, nullable=True)
    character_names = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reformulate_prompt(theme, num_characters, location, era, genre, ending_type, character_names):
    return (f"Create a story with the theme '{theme}', set in '{location}' during the '{era}' era. "
            f"The story should have '{num_characters}' characters. "
            f"The genre is '{genre}' and it should have a '{ending_type}' ending. "
            f"Include characters with the following names: {character_names}. "
            f"Write the story in segments of 4 lines each. Start with the first 4 lines.")

@app.route('/')
def home():
    return "Welcome to the AI Generative Application!"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    theme = data.get('theme', '')
    num_characters = data.get('num_characters', 0)
    location = data.get('location', '')
    era = data.get('era', '')
    genre = data.get('genre', '')
    ending_type = data.get('ending_type', '')
    character_names = data.get('character_names', '')
    num_images = data.get('num_images', 1)

    if not theme or not num_characters:
        return jsonify({'error': 'Theme and number of characters are required'}), 400

    if num_images > 2:
        return jsonify({'error': 'The maximum number of images allowed is 2'}), 400

    session_id = str(uuid.uuid4())
    messages = []

    prompt = reformulate_prompt(theme, num_characters, location, era, genre, ending_type, character_names)

    logger.info(f"Generated prompt: {prompt}")

    try:
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )

        generated_text = response['choices'][0]['message']['content'].strip()
        messages.append({"role": "assistant", "content": generated_text})

        db = next(get_db())
        new_session = ChatSession(session_id=session_id, messages=json.dumps(messages), theme=theme, num_characters=num_characters, location=location, era=era, genre=genre, ending_type=ending_type, character_names=character_names)
        db.add(new_session)
        db.commit()

        logger.info("Story generated successfully.")

        image_response = openai.Image.create(
            prompt=generated_text,
            n=num_images,  # Number of images to generate
            size="1024x1024"
        )

        image_urls = [image['url'] for image in image_response['data']]

        return jsonify({'text': generated_text, 'image_urls': image_urls, 'session_id': session_id})
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/continue', methods=['POST'])
def continue_story():
    data = request.json
    session_id = data.get('session_id')
    theme = data.get('theme', '')
    num_characters = data.get('num_characters', 0)
    location = data.get('location', '')
    era = data.get('era', '')
    genre = data.get('genre', '')
    ending_type = data.get('ending_type', '')
    character_names = data.get('character_names', '')
    num_images = data.get('num_images', 1)

    if not session_id:
        return jsonify({'error': 'Session ID is required'}), 400

    if num_images > 2:
        return jsonify({'error': 'The maximum number of images allowed is 2'}), 400

    db = next(get_db())
    session_data = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    
    if not session_data:
        return jsonify({'error': 'Invalid session ID'}), 400

    # Mettre à jour les champs avec les nouvelles valeurs
    session_data.theme = theme or session_data.theme
    session_data.num_characters = num_characters or session_data.num_characters
    session_data.location = location or session_data.location
    session_data.era = era or session_data.era
    session_data.genre = genre or session_data.genre
    session_data.ending_type = ending_type or session_data.ending_type
    session_data.character_names = character_names or session_data.character_names

    messages = json.loads(session_data.messages)

    try:
        prompt = reformulate_prompt(session_data.theme, session_data.num_characters, session_data.location, session_data.era, session_data.genre, session_data.ending_type, session_data.character_names)
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )

        generated_text = response['choices'][0]['message']['content'].strip()
        messages.append({"role": "assistant", "content": generated_text})

        session_data.messages = json.dumps(messages)
        db.commit()

        logger.info("Story continued successfully.")

        image_response = openai.Image.create(
            prompt=generated_text,
            n=num_images,  # Number of images to generate
            size="1024x1024"
        )

        image_urls = [image['url'] for image in image_response['data']]

        return jsonify({'text': generated_text, 'image_urls': image_urls, 'session_id': session_id,
                        'theme': session_data.theme, 'num_characters': session_data.num_characters, 'location': session_data.location, 'era': session_data.era, 'genre': session_data.genre, 'ending_type': session_data.ending_type, 'character_names': session_data.character_names})
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/correct', methods=['POST'])
def correct():
    data = request.json
    story = data.get('story', '')

    if not story:
        return jsonify({'error': 'Story is required'}), 400

    session_id = str(uuid.uuid4())
    messages = []

    try:
        messages.append({"role": "user", "content": f"Correct any errors in the following story and improve it: {story}"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )

        corrected_text = response['choices'][0]['message']['content'].strip()
        messages.append({"role": "assistant", "content": corrected_text})

        db = next(get_db())
        new_session = ChatSession(session_id=session_id, messages=json.dumps(messages))
        db.add(new_session)
        db.commit()

        logger.info("Story corrected successfully.")

        image_response = openai.Image.create(
            prompt=corrected_text,
            n=1,
            size="1024x1024"
        )

        image_url = image_response['data'][0]['url']

        return jsonify({'corrected_text': corrected_text, 'image_url': image_url, 'session_id': session_id})
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
