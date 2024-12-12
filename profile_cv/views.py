import random
import string
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
# from weasyprint import HTML
from .models import *
from .forms import *
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# from transformers import pipeline

# * |--------------------------------------------------------------------------
# * | Chatbot
# * |--------------------------------------------------------------------------

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
class CVChatbot:
    def __init__(self):
        self.context = {
            'last_topic': None,
            'conversation_history': [],
            'follow_up_questions': {}
        }

        self.responses = {
            'greeting': "👋 Hello! I am your CV assistant. How can I help you today?",
            'help': {
                'main': """I can assist you with the following topics:
                • CV/Resume Creation and Formatting
                • Cover Letter Writing
                • Skills Assessment and Optimization
                • Work Experience Documentation
                • Education and Qualifications
                • Personal Information Management
                • Job Search Strategy
                • Interview Preparation
                
                Just ask me about any of these topics for more details.""",
                'follow_up': [
                    'Which topic interests you the most?',
                    'Would you like specific examples for any of these areas?'
                ]
            },
            'greetings': {
                'english': [
                    "Hi there! How can I assist you with your CV today?",
                    "Welcome! Ready to work on your CV?",
                    "Hello! Let's make your CV stand out!",
                    "Greetings! How may I help you with your resume?"
                ]
            },
            'farewells': {
                'english': [
                    "Goodbye! Good luck with your CV!",
                    "Take care! Feel free to return if you need more CV help!",
                    "Farewell! Wishing you success with your job search!",
                    "Bye! Come back anytime for more CV assistance!"
                ]
            },
            'cv': {
                'main': """Here are key strategies for an effective CV:

                1. Strategic Customization:
                • Tailor your CV for each specific position
                • Mirror the language from the job description
                • Prioritize relevant achievements

                2. Professional Presentation:
                • Maintain consistent formatting
                • Use clear, readable fonts (Arial, Calibri)
                • Include white space for readability

                3. Content Organization:
                • Place most important information first
                • Use bullet points for clarity
                • Keep to 1-2 pages maximum

                4. Achievement Focus:
                • Quantify results where possible
                • Use action verbs
                • Highlight specific contributions

                5. Technical Optimization:
                • Include industry-relevant keywords
                • Use ATS-friendly formatting
                • Save in requested file format""",
                'follow_up': [
                    'Would you like specific examples of action verbs?',
                    'Do you need help with any particular section?'
                ]
            },
            'experience': {
                'main': """Optimize your work experience section with these strategies:

                1. Structure and Format:
                • Use consistent format: [Job Title] - [Company] - [Dates]
                • List positions in reverse chronological order
                • Include location when relevant

                2. Achievement Description:
                • Lead with strong action verbs
                • Focus on measurable results
                • Use format: Action → Task → Result

                3. Quantification:
                • Include specific metrics
                • Add percentages of improvement
                • Mention team sizes managed

                4. Relevancy:
                • Highlight transferable skills
                • Focus on achievements relevant to target role
                • Adjust description length based on relevance""",
                'follow_up': [
                    'Would you like examples of quantified achievements?',
                    'Need help describing a specific role?'
                ]
            },
            'skills': {
                'main': """Create an impactful skills section with these guidelines:

                1. Technical Skills:
                • List relevant software and tools
                • Include proficiency levels
                • Group by category

                2. Soft Skills:
                • Focus on leadership and communication
                • Include problem-solving abilities
                • Highlight team collaboration

                3. Industry-Specific:
                • Add relevant certifications
                • Include specialized training
                • List industry tools mastery

                4. Organization:
                • Prioritize most relevant skills
                • Use clear categorization
                • Update regularly""",
                'follow_up': [
                    'Would you like examples of how to rate your proficiency?',
                    'Need help organizing your skills by category?'
                ]
            },
            'default': {
                'main': """I'm not sure how to help with that query. Try asking about:
                • CV
                • Work experience
                • Skills
                • Education
                • Personal information

                Or type 'help' to see the available topics.""",
                'follow_up': [
                    'Would you like to see the list of topics I can help with?',
                    'Can you rephrase your question?'
                ]
            },
            'farewell': "It was great chatting with you! Feel free to reach out anytime if you have more questions. Have a wonderful day!"
        }

        self.keywords = {
            'cv': ['cv', 'resumé', 'curriculum', 'vitae', 'resume', 'document', 'format', 'layout'],
            'experience': ['experience', 'work', 'job', 'employment', 'position', 'career', 'history'],
            'education': ['education', 'studies', 'degrees', 'training', 'qualifications', 'academic'],
            'skills': ['skills', 'competencies', 'abilities', 'expertise', 'proficiencies', 'capabilities'],
            'personal information': ['personal', 'information', 'details', 'contact', 'data', 'profile'],
        }

    def analyze_intent(self, message):
        message = message.lower().strip()

        if message == 'help':
            return 'help'

        if self.context['last_topic'] and self.is_follow_up_question(message):
            return f"{self.context['last_topic']}_followup"

        # Check for greetings
        if message in ['hello', 'hi', 'hey', 'greetings']:
            return 'greeting'

        # Check for farewells
        if message in ['bye', 'goodbye', 'farewell', 'see you']:
            return 'farewell'

        for key, synonyms in self.keywords.items():
            for synonym in synonyms:
                if synonym in message:
                    return key

        return 'default'

    def is_follow_up_question(self, message):
        follow_up_patterns = [
            'how', 'what', 'can you', 'could you', 'would', 'example',
            'more', 'specific', 'tell me', 'explain'
        ]
        return any(pattern in message for pattern in follow_up_patterns)

    def get_random_response(self, responses):
        import random
        return random.choice(responses)

    def get_follow_up_response(self, topic):
        topic_base = topic.replace('_followup', '')
        follow_ups = self.responses.get(topic_base, {}).get('follow_up', [])
        return self.get_random_response(follow_ups) if follow_ups else None

    def get_bot_response(self, message):
        from datetime import datetime

        self.context['conversation_history'].append({
            'type': 'user',
            'message': message,
            'timestamp': datetime.now()
        })

        intent = self.analyze_intent(message)
        
        if intent == 'greeting':
            response = self.get_random_response(self.responses['greetings']['english'])
        elif intent == 'farewell':
            response = self.get_random_response(self.responses['farewells']['english'])
        elif intent.endswith('_followup'):
            response = self.get_follow_up_response(intent)
        else:
            response = self.responses.get(intent, {}).get('main', self.responses['default']['main'])
            self.context['last_topic'] = intent

        self.context['conversation_history'].append({
            'type': 'bot',
            'message': response,
            'timestamp': datetime.now()
        })

        return response

# Initialize chatbot
chatbot = CVChatbot()

def index(request):
    """Render the chat interface."""
    return render(request, '../../../../../profile_cv/templates/user_cv/user_cv_form.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    """Handle chat messages and return bot responses."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        response = chatbot.get_bot_response(message)
        
        return JsonResponse({
            'response': response,
            'timestamp': str(datetime.now())
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def reset_conversation(request):
    """Reset the chatbot's conversation history."""
    try:
        chatbot.context['last_topic'] = None
        chatbot.context['conversation_history'] = []
        chatbot.context['follow_up_questions'] = {}
        
        return JsonResponse({
            'message': 'Conversation reset successfully',
            'timestamp': str(datetime.now())
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# * |--------------------------------------------------------------------------
# * | Class Profile
# * |--------------------------------------------------------------------------

# ? Función para crear un perfil
@login_required
def profile_create(request, user_id):
    if request.user.id != user_id:
        return redirect("profile_create", request.user.id)
    
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            form.save()
            return redirect("profile_view", user_id)
    else:
        form = ProfileForm()
    return render(request, "profile/profile_form.html", {"form": form, "user": user})

# ? Función para actualizar un perfil
@login_required
def profile_update(request, profile_id):
    profile = get_object_or_404(Profile_CV, id=profile_id)
    if request.method == "POST":
        form = ProfileForm(request.POST,  request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_view", profile.user.id)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profile/profile_form.html", {"form": form, "user": profile.user})

@login_required
def profile_view(request, user_id):
    if request.user.id != user_id:
        return redirect("profile_view", request.user.id)  # Redirige al home o cualquier otra página.
    
    user = get_object_or_404(User, pk=user_id)
    try:
        profile = Profile_CV.objects.get(user=user)
    except Profile_CV.DoesNotExist:
        return redirect('profile_create', user_id)
    
    return render(request, 'profile/profile_view_details.html', {"user": user, "profile": profile})

# * |--------------------------------------------------------------------------
# * | Class WorkExperience
# * |--------------------------------------------------------------------------

# ? Función para crear una experiencia laboral
@login_required
def work_experience_create(request, user_id):
    if request.user.id != user_id:
        return redirect("work_experience_create", request.user.id)
    
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.profile_user = profile
            form.save()
            return redirect("work_experience_list", user_id)
    else:
        form = WorkExperienceForm()
    return render(request, "work_experience/work_experience_form.html", {"form": form, "user": user})

# ? Función para listar las experiencias laborales
@login_required
def work_experience_list(request, user_id):
    if request.user.id != user_id:
        return redirect("work_experience_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    work_experiences = WorkExperience.objects.filter(profile_user=profile)

    return render(request, "work_experience/work_experience_list.html", {"work_experiences": work_experiences, "user": user})

# ? Función para actualizar una experiencia laboral
@login_required
def work_experience_update(request, work_experience_id):
    work_experience = get_object_or_404(WorkExperience, id=work_experience_id)
    user = work_experience.profile_user.user
    if request.method == "POST":
        form = WorkExperienceForm(request.POST, instance=work_experience)
        if form.is_valid():
            form.save()
            return redirect("work_experience_list", user.id)
    else:
        form = WorkExperienceForm(instance=work_experience)
    return render(request, "work_experience/work_experience_form.html", {"form": form, "user": user})

# ? Función para eliminar una experiencia laboral
@login_required
def work_experience_delete(request, work_experience_id):
    work_experience = get_object_or_404(WorkExperience, id=work_experience_id)
    user = work_experience.profile_user.user  # Obtén el usuario directamente desde el perfil
    if request.method == "POST":
        work_experience.delete()
        return redirect("work_experience_list", user.id)
    return render(request, "work_experience/work_experience_confirm_delete.html", {"work_experience": work_experience, "user": user})

# * |--------------------------------------------------------------------------
# * | Class AcademicEducation
# * |--------------------------------------------------------------------------

# ? Función para crear una educación académica
@login_required
def academic_education_create(request, user_id):
    if request.user.id != user_id:
        return redirect("academic_education_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = AcademicEducationForm(request.POST)
        if form.is_valid():
            academic_education = form.save(commit=False)
            academic_education.profile_user = profile
            form.save()
            return redirect("academic_education_list", user_id)
    else:
        form = AcademicEducationForm()
    return render(request, "academic_education/academic_education_form.html", {"form": form, "user": user})

# ? Función para listar las educaciones académicas
@login_required
def academic_education_list(request, user_id):
    if request.user.id != user_id:
        return redirect("academic_education_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    academic_educations = AcademicEducation.objects.filter(profile_user=profile)
    return render(request, "academic_education/academic_education_list.html", {"academic_educations": academic_educations, "user": user})

# ? Función para actualizar una educación académica
@login_required
def academic_education_update(request, academic_education_id):
    academic_education = get_object_or_404(AcademicEducation, id=academic_education_id)
    user = academic_education.profile_user.user  # Obtén el usuario directamente desde el perfil
    if request.method == "POST":
        form = AcademicEducationForm(request.POST, instance=academic_education)
        if form.is_valid():
            form.save()
            return redirect("academic_education_list", user.id)
    else:
        form = AcademicEducationForm(instance=academic_education)
    return render(request, "academic_education/academic_education_form.html", {"form": form, "user": user})

# ? Función para eliminar una educación académica
@login_required
def academic_education_delete(request, academic_education_id):
    academic_education = get_object_or_404(AcademicEducation, id=academic_education_id)
    user = academic_education.profile_user.user  # Obtén el usuario directamente desde el perfil
    if request.method == "POST":
        academic_education.delete()
        return redirect("academic_education_list", user.id)
    return render(request, "academic_education/academic_education_confirm_delete.html", {"academic_education": academic_education, "user": user})

# * |--------------------------------------------------------------------------
# * | Class SoftSkill
# * |--------------------------------------------------------------------------

#? Función para listar las SoftSkills
@login_required
def softskill_list(request, user_id):
    if request.user.id != user_id:
        return redirect("soft_skill_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    softskills = SoftSkillUser.objects.filter(profile_user=profile)
    return render(request, "softskill/softskill_list.html", {"softskills": softskills, "user": user})

#? Función para crear una SoftSkill
@login_required
def softskill_create(request, user_id):
    if request.user.id != user_id:
        return redirect("soft_skill_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = SoftSkillForm(request.POST)
        if form.is_valid():
            soft_skill = form.save(commit=False)
            soft_skill.profile_user = profile
            form.save()
            return redirect("soft_skill_list", user_id)
    else:
        form = SoftSkillForm()
    return render(request, "softskill/softskill_form.html", {"form": form, "user": user})

#? Función para actualizar una SoftSkill
@login_required
def softskill_update(request, soft_skill_id):
    softskill = get_object_or_404(SoftSkillUser, id=soft_skill_id)
    user = softskill.profile_user.user
    if request.method == "POST":
        form = SoftSkillForm(request.POST, instance=softskill)
        if form.is_valid():
            form.save()
            return redirect("soft_skill_list", user.id)
    else:
        form = SoftSkillForm(instance=softskill)
    return render(request, "softskill/softskill_form.html", {"form": form, "user": user})

#? Función para eliminar una SoftSkill
@login_required
def softskill_delete(request, soft_skill_id):
    softskill = get_object_or_404(SoftSkillUser, id=soft_skill_id)
    user = softskill.profile_user.user
    if request.method == "POST":
        softskill.delete()
        return redirect("soft_skill_list", user.id)
    return render(request, "softskill/softskill_confirm_delete.html", {"softskill": softskill, "user": user})

# * |--------------------------------------------------------------------------
# * | Class HardSkill
# * |--------------------------------------------------------------------------

#? Función para listar las HardSkills
@login_required
def hardskill_list(request, user_id):
    if request.user.id != user_id:
        return redirect("hard_skill_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile= get_object_or_404(Profile_CV,  user=user)
    hardskills = HardSkillUser.objects.filter(profile_user = profile)
    return render(request, "hardskill/hardskill_list.html", {"hardskills": hardskills, 'user': user})


#? Función para crear una HardSkill
@login_required
def hardskill_create(request, user_id):
    if request.user.id != user_id:
        return redirect("hard_skill_create", request.user.id)

    user = get_object_or_404(User, id= user_id)
    profile = get_object_or_404(Profile_CV, user = user)
    if request.method == "POST":
        form = HardSkillForm(request.POST)
        if form.is_valid():
            hardskill = form.save(commit  = False)
            hardskill.profile_user = profile
            form.save()
            return redirect("hard_skill_list", user_id)
    else:
        form = HardSkillForm()
    return render(request, "hardskill/hardskill_form.html", {"form": form, 'user': user})

#? Función para eliminar una HardSkill
@login_required
def hardskill_delete(request, hard_skill_id):
    hardskill = get_object_or_404(HardSkillUser, id=hard_skill_id)
    user = hardskill.profile_user.user
    if request.method == "POST":
        hardskill.delete()
        return redirect("hard_skill_list", user.id)
    return render(request, "hardskill/hardskill_confirm_delete.html", {"hardskill": hardskill, "user": user})

#? Función para actualizar una HardSkill
@login_required
def hardskill_update(request, hard_skill_id):
    hardskill = get_object_or_404(HardSkillUser, id=hard_skill_id)
    user = hardskill.profile_user.user
    if request.method == "POST":
        form = HardSkillForm(request.POST, instance=hardskill)
        if form.is_valid():
            form.save()
            return redirect("hard_skill_list", user.id)
    else:
        form = HardSkillForm(instance=hardskill)
    return render(request, "hardskill/hardskill_form.html", {"form": form, "user": user})

# * |--------------------------------------------------------------------------
# * | language
# * |--------------------------------------------------------------------------

#? Función para listar los idiomas
@login_required
def language_list(request, user_id):
    if request.user.id != user_id:
        return redirect("language_list", request.user.id)

    user = get_object_or_404(User, id = user_id)
    profile = get_object_or_404(Profile_CV, user = user)
    languages = LanguageUser.objects.filter(profile_user = profile)
    return render(request, "language/language_list.html", {"languages": languages, 'user': user})

#? Función para crear un idioma
@login_required
def language_create(request, user_id):
    if request.user.id != user_id:
        return redirect("language_create", request.user.id)

    user = get_object_or_404(User, id= user_id)
    profile = get_object_or_404(Profile_CV, user= user)
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit = False)
            language.profile_user = profile
            form.save()
            return redirect("language_list", user_id)
    else:
        form = LanguageForm()
    return render(request, "language/language_form.html", {"form": form, 'user':user})

#? Función para actualizar un idioma
@login_required
def language_update(request, language_id):
    language = get_object_or_404(LanguageUser, id=language_id)
    user = language.profile_user.user
    if request.method == "POST":
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return redirect("language_list", user.id)
    else:
        form = LanguageForm(instance=language)
    return render(request, "language/language_form.html", {"form": form, "user": user})

#? Función para eliminar un idioma
@login_required
def language_delete(request, language_id):
    language = get_object_or_404(LanguageUser, id=language_id)
    user = language.profile_user.user
    if request.method == "POST":
        language.delete()
        return redirect("language_list", user.id)
    return render(request, "language/language_confirm_delete.html", {"language": language, "user": user})

# * |--------------------------------------------------------------------------
# * | Class Volunteering
# * |--------------------------------------------------------------------------

#? Función para listar los voluntariados
@login_required
def volunteering_list(request, user_id):
    if request.user.id != user_id:
        return redirect("volunteering_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    volunteerings = Volunteering.objects.filter(profile_user=profile)
    return render(request, "volunteering/volunteering_list.html", {"volunteerings": volunteerings, "user": user})

#? Función para crear un voluntariado
@login_required
def volunteering_create(request, user_id):
    if request.user.id != user_id:
        return redirect("volunteering_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = VolunteeringForm(request.POST)
        if form.is_valid():
            volunteering = form.save(commit=False)
            volunteering.profile_user = profile
            form.save()
            return redirect("volunteering_list", user_id)
    else:
        form = VolunteeringForm()
    return render(request, "volunteering/volunteering_form.html", {"form": form, "user": user})

#? Función para actualizar un voluntariado
@login_required
def volunteering_update(request, volunteering_id):
    volunteering = get_object_or_404(Volunteering, id=volunteering_id)
    user = volunteering.profile_user.user
    if request.method == "POST":
        form = VolunteeringForm(request.POST, instance=volunteering)
        if form.is_valid():
            form.save()
            return redirect("volunteering_list", user.id)
    else:
        form = VolunteeringForm(instance=volunteering)

    print(user)
    return render(request, "volunteering/volunteering_form.html", {"form": form, "user": user})

#? Función para eliminar un voluntariado
@login_required
def volunteering_delete(request, volunteering_id):
    volunteering = get_object_or_404(Volunteering, id=volunteering_id)
    user = volunteering.profile_user.user
    if request.method == "POST":
        volunteering.delete()
        return redirect("volunteering_list", user.id)
    return render(request, "volunteering/volunteering_confirm_delete.html", {"volunteering": volunteering, "user": user})

# * |--------------------------------------------------------------------------
# * | Class Project
# * |--------------------------------------------------------------------------

#? Función para listar los proyectos
@login_required
def project_list(request, user_id):
    if request.user.id != user_id:
        return redirect("project_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    projects = Project.objects.filter(profile_user=profile)
    return render(request, "project/project_list.html", {"projects": projects, "user": user})

#? Función para crear un proyecto
@login_required
def project_create(request, user_id):
    if request.user.id != user_id:
        return redirect("project_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile_user = profile
            form.save()
            return redirect("project_list", user_id)
    else:
        form = ProjectForm()
    return render(request, "project/project_form.html", {"form": form, "user": user})

#? Función para actualizar un proyecto
@login_required
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = project.profile_user.user
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_list", user.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, "project/project_form.html", {"form": form, "user": user})

#? Función para eliminar un proyecto
@login_required
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = project.profile_user.user
    if request.method == "POST":
        project.delete()
        return redirect("project_list", user.id)
    return render(request, "project/project_confirm_delete.html", {"project": project, "user": user})

# * |--------------------------------------------------------------------------
# * | Class RecognitionAward
# * |--------------------------------------------------------------------------

#? Función para listar los reconocimientos y premios
@login_required
def recognition_award_list(request, user_id):
    if request.user.id != user_id:
        return redirect("recognition_award_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    recognitions_awards = RecognitionAward.objects.filter(profile_user=profile)
    return render(request, "recognitionaward/recognitionaward_list.html", {"recognitions_awards": recognitions_awards, "user": user})

#? Función para crear un reconocimiento o premio
@login_required
def recognition_award_create(request, user_id):
    if request.user.id != user_id:
        return redirect("recognition_award_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = RecognitionForm(request.POST)
        if form.is_valid():
            recognitionaward = form.save(commit=False)
            recognitionaward.profile_user = profile
            form.save()
            return redirect("recognition_award_list", user_id)
    else:
        form = RecognitionForm()
    return render(request, "recognitionaward/recognitionaward_form.html", {"form": form, "user": user})

#? Función para actualizar un reconocimiento o premio
@login_required
def recognition_award_update(request, recognition_award_id):
    recognitionaward = get_object_or_404(RecognitionAward, id=recognition_award_id)
    user = recognitionaward.profile_user.user
    if request.method == "POST":
        form = RecognitionForm(request.POST, instance=recognitionaward)
        if form.is_valid():
            form.save()
            return redirect("recognition_award_list", user.id)
    else:
        form = RecognitionForm(instance=recognitionaward)
    return render(request, "recognitionaward/recognitionaward_form.html", {"form": form, "user": user})

#? Función para eliminar un reconocimiento o premio
@login_required
def recognition_award_delete(request, recognition_award_id):
    recognitionaward = get_object_or_404(RecognitionAward, id=recognition_award_id)
    user = recognitionaward.profile_user.user
    if request.method == "POST":
        recognitionaward.delete()
        return redirect("recognition_award_list", user.id)
    return render(request, "recognitionaward/recognitionaward_confirm_delete.html", {"recognitions_awards": recognitionaward, "user": user})

# * |--------------------------------------------------------------------------
# * | Class Publication
# * |--------------------------------------------------------------------------

#? Función para listar las publicaciones
@login_required
def publication_list(request, user_id):
    if request.user.id != user_id:
        return redirect("publication_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    publications = Publication.objects.filter(profile_user=profile)
    return render(request, "publication/publication_list.html", {"publications": publications, "user": user})

#? Función para crear una publicación
@login_required
def publication_create(request, user_id):
    if request.user.id != user_id:
        return redirect("publication_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    if request.method == "POST":
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.profile_user = profile
            form.save()
            return redirect("publication_list", user_id)
    else:
        form = PublicationForm()
    return render(request, "publication/publication_form.html", {"form": form, "user": user})

#? Función para actualizar una publicación
@login_required
def publication_update(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    user = publication.profile_user.user
    if request.method == "POST":
        form = PublicationForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
            return redirect("publication_list", user.id)
    else:
        form = PublicationForm(instance=publication)
    return render(request, "publication/publication_form.html", {"form": form, "user": user})

#? Función para eliminar una publicación
@login_required
def publication_delete(request, publication_id):
    publication = get_object_or_404(Publication, id=publication_id)
    user = publication.profile_user.user
    if request.method == "POST":
        publication.delete()
        return redirect("publication_list", user.id)
    return render(request, "publication/publication_confirm_delete.html", {"publication": publication, "user": user})

# * |--------------------------------------------------------------------------
# * | User_CV
# * |--------------------------------------------------------------------------

#? Función para listar los CV
@login_required
def user_cv_list(request, user_id):
    if request.user.id != user_id:
        return redirect("user_cv_list", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile_CV, user=user)
    user_cv = User_cv.objects.filter(profile_user=profile)
    return render(request, "user_cv/user_cv_list.html", {"user_cv": user_cv, "profile": profile, "user": user})

#? Función para crear un CV
@login_required
def user_cv_create(request, user_id):
    if request.user.id != user_id:
        return redirect("user_cv_create", request.user.id)

    user = get_object_or_404(User, id=user_id)
    profile_cv = get_object_or_404(Profile_CV, user=user)
    work_experiences = WorkExperience.objects.filter(profile_user=profile_cv)
    academic_educations = AcademicEducation.objects.filter(profile_user=profile_cv)
    hard_skills = HardSkillUser.objects.filter(profile_user=profile_cv)
    soft_skills = SoftSkillUser.objects.filter(profile_user=profile_cv)
    languages = LanguageUser.objects.filter(profile_user=profile_cv)
    categories = CategoryUser.objects.filter(profile_user=profile_cv)
    sectors = SectorUser.objects.filter(profile_user=profile_cv)
    incorporations = IncorporationUser.objects.filter(profile_user=profile_cv)
    volunteerings = Volunteering.objects.filter(profile_user=profile_cv)
    projects = Project.objects.filter(profile_user=profile_cv)
    publications = Publication.objects.filter(profile_user=profile_cv)
    recognitions_awards = RecognitionAward.objects.filter(profile_user=profile_cv)

    random_numbers = ''.join(random.choices(string.digits, k=4))
    initial_urlCV = f"{profile_cv.user.username}-{random_numbers}"

    if request.method == "POST":
        print(request.POST)
        form = UserCvForm(request.POST)
        if form.is_valid():
            user_cv = form.save(commit=False)
            user_cv.profile_user = profile_cv
            user_cv.urlCV = request.POST.get('initial_urlCV')
            user_cv.save()

            # Guardar relaciones
            selected_experiences = request.POST.getlist('work_experiences')
            for experience_id in selected_experiences:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    work_experience_id=experience_id
                )

            selected_academic_educations = request.POST.getlist('academic_educations')
            for education_id in selected_academic_educations:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    academic_education_id=education_id
                )

            selected_hard_skills = request.POST.getlist('hard_skills')
            for skill_id in selected_hard_skills:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    hard_skill_id=skill_id
                )

            selected_soft_skills = request.POST.getlist('soft_skills')
            for skill_id in selected_soft_skills:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    soft_skill_id=skill_id
                )

            selected_languages = request.POST.getlist('languages')
            for language_id in selected_languages:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    language_id=language_id
                )

            selected_categories = request.POST.getlist('categories')
            for category_id in selected_categories:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    category_id=category_id
                )

            selected_sectors = request.POST.getlist('sectors')
            for sector_id in selected_sectors:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    sector_id=sector_id
                )

            selected_incorporations = request.POST.getlist('incorporations')
            for incorporation_id in selected_incorporations:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    incorporation_id=incorporation_id
                )

            selected_volunteerings = request.POST.getlist('volunteerings')
            for volunteering_id in selected_volunteerings:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    volunteering_id=volunteering_id
                )

            selected_projects = request.POST.getlist('projects')
            for project_id in selected_projects:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    project_id=project_id
                )

            selected_publications = request.POST.getlist('publications')
            for publication_id in selected_publications:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    publication_id=publication_id
                )

            selected_recognitions = request.POST.getlist('recognitions_awards')
            for recognition_id in selected_recognitions:
                UserCvRelation.objects.create(
                    user_cv=user_cv,
                    recognition_award_id=recognition_id
                )

            return redirect("user_cv_list", user.id)
    else:
        form = UserCvForm(initial={'urlCV': initial_urlCV})

    context = {
        "user": user,
        'form': form,
        'profile_cv': profile_cv,
        'work_experiences': work_experiences,
        'academic_educations': academic_educations,
        'hard_skills': hard_skills,
        'soft_skills': soft_skills,
        'languages': languages,
        'categories': categories,
        'sectors': sectors,
        'incorporations': incorporations,
        'volunteerings': volunteerings,
        'projects': projects,
        'publications': publications,
        "courses": profile_cv.user.enrolled_courses.filter(status__name='completed'),
        'recognitions_awards': recognitions_awards,
        'full_urlCV': f"user_cvs/view/{initial_urlCV}",
        "initial_urlCV": initial_urlCV
    }

    return render(request, "user_cv/user_cv_form.html", context)

#? Función para actualizar un CV
@login_required
def user_cv_update(request, user_cv_id):
    user_cv = get_object_or_404(User_cv, id=user_cv_id)
    profile_cv = get_object_or_404(Profile_CV, id= user_cv.profile_user.id)
    user = profile_cv.user
    if request.method == "POST":
        form = UserCvForm(request.POST, instance=user_cv)
        if form.is_valid():
            form.save()
            return redirect("user_cv_list", user.id)  # Pasa el profile_id aquí
    else:
        form = UserCvForm(instance=user_cv)
    return render(request, "user_cv/user_cv_form.html", {"form": form, "user_cv": user_cv, "profile_cv": profile_cv, "user": user})

#? Función para eliminar un CV
@login_required
def user_cv_delete(request, user_cv_id):
    user_cv = get_object_or_404(User_cv, id=user_cv_id)
    user = user_cv.profile_user.user
    if request.method == "POST":
        user_cv.delete()
        return redirect("user_cv_list", user.pk)  # Pasa el profile_id aquí
    return render(request, "user_cv/user_cv_confirm_delete.html", {"user_cv": user_cv, "user": user})

#? Función para ver los detalles de un CV
@login_required
def user_cv_view_details(request, user_cv_id, profile_cv_id):
    user_cv = get_object_or_404(User_cv, id=user_cv_id)
    profile_cv = get_object_or_404(Profile_CV, id=profile_cv_id)

    # Filtrar solo los campos asociadas al User_cv
    user_cv_relations = UserCvRelation.objects.filter(user_cv=user_cv)

    work_experiences = WorkExperience.objects.filter(id__in=user_cv_relations.values('work_experience'))
    academic_educations = AcademicEducation.objects.filter(id__in=user_cv_relations.values('academic_education'))
    hard_skills = HardSkillUser.objects.filter(id__in=user_cv_relations.values('hard_skill'))
    soft_skills = SoftSkillUser.objects.filter(id__in=user_cv_relations.values('soft_skill'))
    languages = LanguageUser.objects.filter(id__in=user_cv_relations.values('language'))
    categories = CategoryUser.objects.filter(id__in=user_cv_relations.values('category'))
    sectors = SectorUser.objects.filter(id__in=user_cv_relations.values('sector'))
    incorporations = IncorporationUser.objects.filter(id__in=user_cv_relations.values('incorporation'))
    volunteerings = Volunteering.objects.filter(id__in=user_cv_relations.values('volunteering'))
    projects = Project.objects.filter(id__in=user_cv_relations.values('project'))
    publications = Publication.objects.filter(id__in=user_cv_relations.values('publication'))
    recognitions_awards = RecognitionAward.objects.filter(id__in=user_cv_relations.values('recognition_award'))

    context = {
        'user_cv': user_cv,
        'profile_cv': profile_cv,
        'work_experiences': work_experiences,
        'academic_educations': academic_educations,
        'hard_skills': hard_skills,
        'soft_skills': soft_skills,
        'languages': languages,
        'categories': categories,
        'sectors': sectors,
        'incorporations': incorporations,
        'volunteerings': volunteerings,
        'projects': projects,
        'publications': publications,
        'recognitions_awards': recognitions_awards,
    }

    return render(request, 'user_cv/user_cv_view_details.html', context)

@login_required
def user_cv_view(request, url):
    user_cv = get_object_or_404(User_cv, urlCV=url)
    profile_cv_id = user_cv.profile_user.id
    return redirect('user_cv_view_details', user_cv_id=user_cv.id, profile_cv_id=profile_cv_id)

@login_required
def user_cv_pdf_view(request, user_cv_id, profile_cv_id):
    # user_cv = get_object_or_404(User_cv, id=user_cv_id)
    # profile_cv = get_object_or_404(Profile_CV, id=profile_cv_id)
    # work_experiences = WorkExperience.objects.filter(profile_user=profile_cv)
    # academic_educations = AcademicEducation.objects.filter(profile_user=profile_cv)
    # hard_skills = HardSkillUser.objects.filter(profile_user=profile_cv)
    # soft_skills = SoftSkillUser.objects.filter(profile_user=profile_cv)
    # languages = LanguageUser.objects.filter(profile_user=profile_cv)
    # categories = CategoryUser.objects.filter(profile_user=profile_cv)
    # sectors = SectorUser.objects.filter(profile_user=profile_cv)
    # incorporations = IncorporationUser.objects.filter(profile_user=profile_cv)
    # volunteerings = Volunteering.objects.filter(profile_user=profile_cv)
    # projects = Project.objects.filter(profile_user=profile_cv)
    # publications = Publication.objects.filter(profile_user=profile_cv)
    # recognitions_awards = RecognitionAward.objects.filter(profile_user=profile_cv)

    # context = {
    #     'user_cv': user_cv,
    #     'profile_cv': profile_cv,
    #     'work_experiences': work_experiences,
    #     'academic_educations': academic_educations,
    #     'hard_skills': hard_skills,
    #     'soft_skills': soft_skills,
    #     'languages': languages,
    #     'categories': categories,
    #     'sectors': sectors,
    #     'incorporations': incorporations,
    #     'volunteerings': volunteerings,
    #     'projects': projects,
    #     'publications': publications,
    #     'recognitions_awards': recognitions_awards,
    # }

    # template = get_template('user_cv/user_cv_view_details.html')
    # html_content = template.render(context)

    # pdf_file = HTML(string=html_content).write_pdf()

    # response = HttpResponse(pdf_file, content_type='application/pdf')
    # response['Content-Disposition'] = "inline; filename='user_cv.pdf'"

    # return response
    pass