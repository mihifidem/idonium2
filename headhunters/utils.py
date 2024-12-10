import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import json

# Rutas de los archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'chatbot', 'enhanced_chat_model.keras')
TOKENIZER_PATH = os.path.join(BASE_DIR, 'chatbot', 'tokenizer.pickle')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'chatbot', 'label_encoder.pickle')
RESPONSES_PATH = os.path.join(BASE_DIR, 'chatbot', 'intents2.json')

# Cargar modelo
model = tf.keras.models.load_model(MODEL_PATH)

# Cargar tokenizador y label encoder
with open(TOKENIZER_PATH, 'rb') as handle:
    tokenizer = pickle.load(handle)

with open(LABEL_ENCODER_PATH, 'rb') as handle:
    lbl_encoder = pickle.load(handle)

# Cargar respuestas
with open(RESPONSES_PATH, encoding="utf-8") as file:
    data = json.load(file)

responses = {intent['tag']: intent['responses'] for intent in data['intents']}

# Parámetros
MAX_LEN = 20

# Función para preprocesar entrada
def preprocess_input(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    return pad_sequences(sequence, truncating='post', maxlen=MAX_LEN)

# Función para obtener respuesta
def get_response(user_input):
    try:
        # Preprocesar
        input_data = preprocess_input(user_input)
        
        # Predicción
        pred = model.predict(input_data)
        predicted_label = np.argmax(pred, axis=1)
        label = lbl_encoder.inverse_transform(predicted_label)[0]

        # Obtener respuesta
        if label not in responses:
            return "Lo siento, no tengo una respuesta para eso."
        return random.choice(responses[label])
    except Exception as e:
        return f" error: {str(e)}"
