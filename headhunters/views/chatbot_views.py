
import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import json
from django.shortcuts import render
from django.http import JsonResponse
from tensorflow.keras.models import load_model

model = load_model('headhunters/chatbot/enhanced_chat_model.keras')
with open('headhunters/chatbot/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('headhunters/chatbot/label_encoder.pickle', 'rb') as handle:
    label_encoder = pickle.load(handle)
with open('headhunters/chatbot/intents2.json',encoding='utf-8') as file:
    intents = json.load(file)

responses = {}
for intent in intents['intents']:
    responses[intent['tag']] = intent['responses']

def preprocess_input(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, truncating='post', maxlen=max_len)
    return padded_sequence

max_len = 20
vocab_size = 1000
oov_token = "<OOV>"

# Function to generate chatbot response
def chatbot_response(user_input):
     # Preprocesar la entrada
    input_data = preprocess_input(user_input)
    
    # Predecir la etiqueta
    pred = model.predict(input_data)
    predicted_label = np.argmax(pred, axis=1)
    
    # Decodificar la etiqueta
    label = label_encoder.inverse_transform(predicted_label)[0]
    
    # Obtener las posibles respuestas para esta etiqueta
    possible_responses = responses[label]
    
    # Elegir una respuesta aleatoria
    response = random.choice(possible_responses)
    
    return response
    # try:
    #     print(f"User Message: {message}")

    #     # Tokenize and preprocess the input message (match training preprocessing)
    #     input_data = tokenizer.texts_to_sequences([message])  # Use texts_to_sequences
    #     input_data = pad_sequences(input_data, maxlen=20, padding='post')  # Set maxlen=11 to match training

    #     print(f"Processed Input Shape: {input_data.shape}")

    #     # Verify input shape matches training shape
    #     expected_input_shape = model.input_shape[1]
    #     if input_data.shape[1] != expected_input_shape:
    #         print(f"Input shape mismatch. Expected: {expected_input_shape}, Got: {input_data.shape[1]}")
    #         return "Sorry, I'm having trouble understanding that."

    #     # Reshape input to match expected shape (batch_size, sequence_length, 1)
    #     input_data = np.reshape(input_data, (input_data.shape[0], input_data.shape[1], 1))

    #     # Predict with the model
    #     prediction = model.predict(input_data)
    #     print(f"Prediction Probabilities: {prediction}")

    #     # Extract the most probable tag and its confidence
    #     predicted_index = np.argmax(prediction)
    #     predicted_confidence = prediction[0][predicted_index]
    #     predicted_tag = label_encoder.inverse_transform([predicted_index])[0]

    #     print(f"Predicted Tag: {predicted_tag}, Confidence: {predicted_confidence}")

    #     # Confidence threshold to filter uncertain responses
    #     confidence_threshold = 0.7  # Adjust based on testing
    #     if predicted_confidence < confidence_threshold:
    #         return "I'm not sure. Can you clarify or ask in a different way?"

    #     # Find a response matching the predicted tag
    #     for intent in intents['intents']:
    #         if intent['tag'] == predicted_tag:
    #             response = np.random.choice(intent['responses'])
    #             print(f"Selected Response: {response}")
    #             return response

    #     # Default fallback if no match is found
    #     return "I understand your message, but I don't have an appropriate response."

    # except Exception as e:
    #     print(f"Error in chatbot_response: {e}")
    #     return "Something went wrong. Please try again later."
    
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Get the message from the request
        user_message = data.get('message', '')  # Extract the message
        response = chatbot_response(user_message)  # Get chatbot's response
        return JsonResponse({'bot_message': response}, json_dumps_params={'ensure_ascii': False})  # Return the response as JSON
    return JsonResponse({'error': 'Invalid request'}, status=400)  # Handle invalid requests

# Render the chatbot page for GET requests
def chatbot_page(request):
    return render(request, 'chatbot/chatbot.html')  # Render the new HTML page