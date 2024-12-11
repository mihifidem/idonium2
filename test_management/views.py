from django.shortcuts import render, redirect, get_object_or_404
import json
import os
import pickle
from datetime import datetime

import nltk
import numpy as np
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from keras.src.utils import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

from .forms import TestForm, QuestionForm
from .models import Test, UserAnswer, TestResult


# TEST CREATION
@login_required
def create_test(request):
    if not request.user.is_headhunter:
        return redirect("dashboard")

    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user
            test.save()
            return redirect("add_questions", test_id=test.id)
    else:
        form = TestForm()
    return render(request, "test_platform/create_test.html", {"form": form})

@login_required
def add_questions(request, test_id):
    test = get_object_or_404(Test, id=test_id, created_by=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test
            question.save()
            return redirect("add_questions", test_id=test.id)
    else:
        form = QuestionForm()
    return render(request, "test_platform/add_questions.html", {"form": form, "test": test})

# TEST TAKING AND SUBMISSION
@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == "POST":
        score = 0
        for question in test.questions.all():
            user_answer = request.POST.get(f"question_{question.id}")
            is_correct = user_answer == question.correct_answer
            UserAnswer.objects.create(
                user=request.user, question=question, selected_answer=user_answer, is_correct=is_correct
            )
            score += 1 if is_correct else 0
        TestResult.objects.create(user=request.user, test=test, score=score)
        return redirect("dashboard")
    return render(request, "test_platform/take_test.html", {"test": test})

def load_quiz(file_name):
    """Load quiz data from the selected JSON file."""
    quiz_path = os.path.join(settings.BASE_DIR, "test_management", "static", file_name)
    try:
        with open(quiz_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# View to display quiz selection form
def quiz_view(request):
    if request.method == 'POST':
        quiz_file = request.POST.get('quiz_file')

        if not quiz_file:
            return render(request, 'quiz/quiz_select.html', {
                'error': 'No quiz file selected. Please select a quiz from the list.',
                'quiz_files': [
                    'CSS.json',
                    'Django.json',
                    'HTML.json',
                    'Numpy.json',
                    'SQL.json',
                    'Python-1.json',
                    'Python-2.json',
                    'Python-3.json',
                    'Soft Skills.json',
                    'Belbin.json',
                    'Git.json',
                    'JavaScript.json'
                ]
            })

        quiz_data = load_quiz(quiz_file)

        if quiz_data:
            return render(request, 'quiz/quiz_form.html', {'quiz_data': quiz_data, 'quiz_file': quiz_file})
        else:
            return render(request, 'quiz/quiz_select.html', {
                'error': f'Quiz file "{quiz_file}" not found. Please select a valid quiz.',
                'quiz_files': [
                    'CSS.json',
                    'Django.json',
                    'HTML.json',
                    'Numpy.json',
                    'SQL.json',
                    'Python-1.json',
                    'Python-2.json',
                    'Python-3.json',
                    'Soft Skills.json',
                    'Belbin.json',
                    'Git.json',
                    'JavaScript.json'
                ]
            })

    else:
        quiz_files = [
            'CSS.json',
            'Django.json',
            'HTML.json',
            'Numpy.json',
            'SQL.json',
            'Python-1.json',
            'Python-2.json',
            'Python-3.json',
            'Soft Skills.json',
            'Belbin.json',
            'Git.json',
            'JavaScript.json'
        ]
        return render(request, 'quiz/quiz_select.html', {'quiz_files': quiz_files})


# View to handle quiz submission and show results
def submit_quiz(request):
    if request.method == 'POST':
        quiz_file = request.POST.get('quiz_file')
        quiz_data = load_quiz(quiz_file)

        if not quiz_data:
            return render(request, 'quiz/quiz_form.html', {'error': 'Quiz file not found'})

        score = 0
        total_questions = len(quiz_data)
        wrong_questions = []

        # Calculate duration
        start_time = float(request.POST.get('start_time'))
        duration_seconds = (datetime.now().timestamp() - start_time)
        duration_minutes = int(duration_seconds // 60)
        duration_seconds %= 60

        for question in quiz_data:
            question_id = quiz_data.index(question) + 1
            selected_answer = request.POST.get(f'question_{question_id}')

            if selected_answer == question['correct_answer']:
                score += 1
            else:
                wrong_questions.append({
                    'question': question['question'],
                    'selected_answer': selected_answer,
                    'correct_answer': question['correct_answer']
                })

        score_percentage = (score / total_questions) * 100 if total_questions else 0

        return render(request, 'quiz/results.html', {
            'score': score,
            'total': total_questions,
            'wrong_questions': wrong_questions,
            'score_percentage': score_percentage,
            'duration_minutes': duration_minutes,
            'duration_seconds': int(duration_seconds)
        })

    return render(request, 'quiz/quiz_form.html', {'error': 'Invalid form submission'})

model = load_model('test_management/chatbot/belbin/chatbot_model.keras')
with open('test_management/chatbot/belbin/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('test_management/chatbot/belbin/label_encoder.pickle', 'rb') as handle:
    label_encoder = pickle.load(handle)
with open('test_management/chatbot/belbin/intents-Belbin.json') as file:
    intents = json.load(file)

# Function to generate chatbot response
def chatbot_response(message):
    try:
        print(f"User Message: {message}")

        # Tokenize and preprocess the input message (match training preprocessing)
        input_data = tokenizer.texts_to_sequences([message])  # Use texts_to_sequences
        input_data = pad_sequences(input_data, maxlen=11, padding='post')  # Set maxlen=11 to match training

        print(f"Processed Input Shape: {input_data.shape}")

        # Verify input shape matches training shape
        expected_input_shape = model.input_shape[1]
        if input_data.shape[1] != expected_input_shape:
            print(f"Input shape mismatch. Expected: {expected_input_shape}, Got: {input_data.shape[1]}")
            return "Sorry, I'm having trouble understanding that."

        # Reshape input to match expected shape (batch_size, sequence_length, 1)
        input_data = np.reshape(input_data, (input_data.shape[0], input_data.shape[1], 1))

        # Predict with the model
        prediction = model.predict(input_data)
        print(f"Prediction Probabilities: {prediction}")

        # Extract the most probable tag and its confidence
        predicted_index = np.argmax(prediction)
        predicted_confidence = prediction[0][predicted_index]
        predicted_tag = label_encoder.inverse_transform([predicted_index])[0]

        print(f"Predicted Tag: {predicted_tag}, Confidence: {predicted_confidence}")

        # Confidence threshold to filter uncertain responses
        confidence_threshold = 0.7  # Adjust based on testing
        if predicted_confidence < confidence_threshold:
            return "I'm not sure. Can you clarify or ask in a different way?"

        # Find a response matching the predicted tag
        for intent in intents['intents']:
            if intent['tag'] == predicted_tag:
                response = np.random.choice(intent['responses'])
                print(f"Selected Response: {response}")
                return response

        # Default fallback if no match is found
        return "I understand your message, but I don't have an appropriate response."

    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        return "Something went wrong. Please try again later."


# Chatbot view to handle chatbot messages (POST requests)
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Get the message from the request
        user_message = data.get('message', '')  # Extract the message
        response = chatbot_response(user_message)  # Get chatbot's response
        return JsonResponse({'bot_message': response})  # Return the response as JSON
    return JsonResponse({'error': 'Invalid request'}, status=400)  # Handle invalid requests

# Render the chatbot page for GET requests
def chatbot_page(request):
    return render(request, 'quiz/chatbot.html')  # Render the new HTML page