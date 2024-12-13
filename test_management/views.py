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
from django.views.decorators.csrf import ensure_csrf_cookie

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

def load_json_file(file_path):
    """
    Loads a JSON file from the specified path.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

# View to display quiz selection form
import os
from django.shortcuts import render
from django.contrib import messages # Assuming you have this utility for loading JSON files

def quiz_view(request):
    """
    Permite al usuario seleccionar y tomar un cuestionario.
    """
    # Lista de archivos con extensión .json
    quiz_files = [
        'CSS.json', 'Django.json', 'HTML.json', 'Numpy.json',
        'SQL.json', 'Python-1.json', 'Python-2.json', 'Python-3.json',
        'Soft Skills.json', 'Belbin.json', 'Git.json', 'JavaScript.json'
    ]

    # Quitar extensiones para mostrar en la plantilla
    quiz_files_no_ext = [os.path.splitext(file)[0] for file in quiz_files]

    if request.method == 'POST':
        # Recuperar el archivo seleccionado sin la extensión
        quiz_file = request.POST.get('quiz_file')

        if not quiz_file:
            return render(request, 'quiz/quiz_select.html', {
                'error': 'No quiz file selected. Please select a quiz from the list.',
                'quiz_files': quiz_files_no_ext
            })

        quiz_file_with_ext = f"{quiz_file}.json"

        # Intentar cargar los datos del archivo seleccionado
        quiz_data = load_json_file(f"test_management/static/{quiz_file_with_ext}")
        if quiz_data:
            return render(request, 'quiz/quiz_form.html', {'quiz_data': quiz_data, 'quiz_file': quiz_file})
        
        else:
            messages.error(request, f"Archivo {quiz_file_with_ext} no encontrado.")
            return render(request, 'quiz/quiz_select.html', {
                'error': f'Quiz file "{quiz_file}" not found. Please select a valid quiz.',
                'quiz_files': quiz_files_no_ext
            })

    return render(request, 'quiz/quiz_select.html', {'quiz_files': quiz_files_no_ext})


def submit_quiz(request):
    if request.method == 'POST':
        quiz_file = request.POST.get('quiz_file') + ".json"
        quiz_data = load_json_file(f"test_management/static/{quiz_file}")

        if not quiz_data:
            return render(request, 'quiz/quiz_form.html', {'error': 'Quiz file not found'})

        # Variables para resultados
        total_questions = len(quiz_data)
        wrong_questions = []
        unanswered_questions = []
        category_scores = {}

        # Calcular duración
        start_time = float(request.POST.get('start_time'))
        duration_seconds = (datetime.now().timestamp() - start_time)
        duration_minutes = int(duration_seconds // 60)
        duration_seconds %= 60

        if quiz_file in ['Soft Skills.json', 'Belbin.json']:
            # Lógica personalizada para Belbin y SoftSkills
            category_scores = {category: 0 for category in set(q['category'] for q in quiz_data)}
            for question_id, question in enumerate(quiz_data, start=1):
                selected_answer = request.POST.get(f'question_{question_id}')
                if not selected_answer:
                    unanswered_questions.append({
                        'question': question['question'],
                        'correct_answer': question['correct_answer']
                    })
                    continue

                weights = {item['answer']: item['weight'] for item in question.get('answer_weights', [])}
                if selected_answer in weights:
                    category_scores[question['category']] += weights[selected_answer]
        else:
            # Lógica existente para otros tests
            score = 0
            for question_id, question in enumerate(quiz_data, start=1):
                selected_answer = request.POST.get(f'question_{question_id}')
                if not selected_answer:
                    unanswered_questions.append({
                        'question': question['question'],
                        'correct_answer': question['correct_answer']
                    })
                    continue

                if selected_answer == question['correct_answer']:
                    score += 1
                else:
                    wrong_questions.append({
                        'question': question['question'],
                        'selected_answer': selected_answer,
                        'correct_answer': question['correct_answer'],
                        'improvement': question.get('improvement', 'No improvement available')
                    })

            score_percentage = (score / total_questions) * 100 if total_questions else 0

        return render(request, 'quiz/results.html', {
            'score': score if quiz_file not in ['Soft Skills.json', 'Belbin.json'] else None,
            'total': total_questions,
            'wrong_questions': wrong_questions,
            'unanswered_questions': unanswered_questions,
            'category_scores': category_scores if quiz_file in ['Soft Skills.json', 'Belbin.json'] else None,
            'duration_minutes': duration_minutes,
            'duration_seconds': int(duration_seconds)
        })

    return render(request, 'quiz/quiz_form.html', {'error': 'Invalid form submission'})


# Function to load resources for the selected category
def load_chatbot_resources(category):
    try:
        if category == "belbin":
            model_path = 'test_management/chatbot/belbin/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/belbin/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/belbin/label_encoder.pickle'
            intents_path = 'test_management/chatbot/belbin/intents-belbin.json'

        elif category == "git":
            model_path = 'test_management/chatbot/git/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/git/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/git/label_encoder.pickle'
            intents_path = 'test_management/chatbot/git/intents-git.json'

        elif category == "soft skills":
            model_path = 'test_management/chatbot/softskills/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/softskills/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/softskills/label_encoder.pickle'
            intents_path = 'test_management/chatbot/softskills/intents-softskills.json'

        elif category == "css":
            model_path = 'test_management/chatbot/css/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/css/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/css/label_encoder.pickle'
            intents_path = 'test_management/chatbot/css/intents-css.json'

        elif category == "html":
            model_path = 'test_management/chatbot/html/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/html/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/html/label_encoder.pickle'
            intents_path = 'test_management/chatbot/html/intents-html.json'

        elif category == "javascript":
            model_path = 'test_management/chatbot/js/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/js/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/js/label_encoder.pickle'
            intents_path = 'test_management/chatbot/js/intents-js.json'

        elif category == "python-1":
            model_path = 'test_management/chatbot/python/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/python/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/python/label_encoder.pickle'
            intents_path = 'test_management/chatbot/python/intents-python.json'

        elif category == "python-2":
            model_path = 'test_management/chatbot/python/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/python/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/python/label_encoder.pickle'
            intents_path = 'test_management/chatbot/python/intents-python.json'

        elif category == "python-3":
            model_path = 'test_management/chatbot/python/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/python/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/python/label_encoder.pickle'
            intents_path = 'test_management/chatbot/python/intents-python.json'

        elif category == "django":
            model_path = 'test_management/chatbot/django/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/django/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/django/label_encoder.pickle'
            intents_path = 'test_management/chatbot/django/intents-django.json'

        elif category == "numpy":
            model_path = 'test_management/chatbot/numpy/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/numpy/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/numpy/label_encoder.pickle'
            intents_path = 'test_management/chatbot/numpy/intents-numpy.json'

        elif category == "sql":
            model_path = 'test_management/chatbot/sql/chatbot_model.keras'
            tokenizer_path = 'test_management/chatbot/sql/tokenizer.pickle'
            label_encoder_path = 'test_management/chatbot/sql/label_encoder.pickle'
            intents_path = 'test_management/chatbot/sql/intents-sql.json'

        else:
            raise ValueError("Invalid category")

        print(f"Loading model from {model_path}")
        model = load_model(model_path)

        print(f"Loading tokenizer from {tokenizer_path}")
        with open(tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)

        print(f"Loading label encoder from {label_encoder_path}")
        with open(label_encoder_path, 'rb') as handle:
            label_encoder = pickle.load(handle)

        print(f"Loading intents from {intents_path}")
        with open(intents_path) as file:
            intents = json.load(file)

        return model, tokenizer, label_encoder, intents
    except Exception as e:
        print(f"Error in load_chatbot_resources: {e}")
        raise



# Function to generate chatbot response based on the input message and category
def chatbot_response(message, category):
    try:
        category = category.lower()
        model, tokenizer, label_encoder, intents = load_chatbot_resources(category)

        print("Model, tokenizer, label_encoder, and intents loaded successfully.")

        # Tokenize and preprocess the input message
        
        input_data = tokenizer.texts_to_sequences([message])
        expected_input_shape = model.input_shape[1]  # Get maxlen from the model

        input_data = pad_sequences(input_data, maxlen=expected_input_shape, padding='post')

        # Verify input shape matches the model's expected shape
        print(f"Input data shape: {input_data.shape}")
        expected_input_shape = model.input_shape[1]
        if input_data.shape[1] != expected_input_shape:
            return "Sorry, I'm having trouble understanding that."

        # Predict with the model
        prediction = model.predict(input_data)
        predicted_index = np.argmax(prediction)
        predicted_confidence = prediction[0][predicted_index]
        predicted_tag = label_encoder.inverse_transform([predicted_index])[0]

        # Confidence threshold
        confidence_threshold = 0.7
        if predicted_confidence < confidence_threshold:
            return "I'm not sure. Can you clarify or ask in a different way?"

        # Find a response matching the predicted tag
        for intent in intents["intents"]:
            if intent["tag"] == predicted_tag:
                return np.random.choice(intent["responses"])

        return "I understand your message, but I don't have an appropriate response."
    except Exception as e:
        print(f"Error in chatbot_response: {e}")
        return "Something went wrong. Please try again later."
# Chatbot view to handle user messages and return bot responses modified 19:14
@ensure_csrf_cookie
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        category = data.get("category", "belbin")  # Default to 'belbin'

        if user_message:
            response = chatbot_response(user_message, category)
            return JsonResponse({"bot_message": response})

        return JsonResponse({"bot_message": "No message provided"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

# Render the chatbot page for GET requests
def chatbot_page(request):
    categories = ["belbin", "git", "soft skills", "css", "javascript", "python-1",
                  "python-2", "python-3", "html", "django", "numpy", "sql"]
    return render(request, "quiz/quiz_form.html", {"categories": categories})  # Render the HTML page
