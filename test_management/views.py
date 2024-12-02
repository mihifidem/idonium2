from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Test, UserAnswer, TestResult
from .forms import  TestForm, QuestionForm
from django.conf import settings
import os
import json
from datetime import datetime

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



