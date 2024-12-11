from django import forms
from .models import *

# Form to represent a profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile_CV
        fields = [
            "user",
            "img_1_profile",
            "img_2_profile",
            "img_3_profile",
            "img_4_profile",
            "address",
            "phone_1",
            "phone_2",
            "email_1",
            "email_2",
            "dni",
            "biography",
            "open_to_work",
            "vehicle",
            "disability",
            "disability_percentage",
            "incorporation",
            "sector",
            "category",
            "work_experiences",
            "hard_skills",
            "soft_skills",
            "languages",
            "academic_educations",
            "volunteerings",
            "projects",
            "publications",
            "recognitions_awards",
            "certifications_courses",
        ]

# Form to represent a work experience
class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = [
            "job_title",
            "start_date",
            "end_date",
            "current_job",
            "company_name",
            "description",
            "achievements",
            "references",
        ]

# Form to represent an academic education
class AcademicEducationForm(forms.ModelForm):
    class Meta:
        model = AcademicEducation
        fields = [
            "title",
            "academy_name",
            "start_date",
            "end_date",
            "current_education",
            "references",
        ]

# Form to represent a hard skill
class HardSkillForm(forms.ModelForm):
    class Meta:
        model = HardSkillUser
        fields = ["hard_skill", "description", "level_skill"]

# Form to represent a soft skill
class SoftSkillForm(forms.ModelForm):
    class Meta:
        model = SoftSkillUser
        fields = ["soft_skill", "description"]

# Form to represent a language
class LanguageForm(forms.ModelForm):
    class Meta:
        model = LanguageUser
        fields = ["language", "level", "certifications"]

# Form to represent a volunteering
class VolunteeringForm(forms.ModelForm):
    class Meta:
        model = Volunteering
        fields = [
            "volunteering_position",
            "start_date",
            "end_date",
            "current_volunteering",
            "entity_name",
            "description",
            "achievements",
            "references",
        ]

# Form to represent a project
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "link"]

# Form to represent a publication
class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["doi", "url", "role", "name"]

# Form to represent a recognition or award
class RecognitionForm(forms.ModelForm):
    class Meta:
        model = RecognitionAward
        fields = ["name", "entity", "description"]

#form to represent a user cv
class ToggleButtonWidget(forms.CheckboxInput):
    template_name = 'user_cv/button.html'

class ReadOnlyWidget(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'readonly': 'readonly'}
        super().__init__(*args, **kwargs)

class UserCvForm(forms.ModelForm):
    class Meta:
        model = User_cv
        fields = [
            "urlCV",
            "template",
            "has_img_profile",
            "has_address",
            "has_phone_1",
            "has_phone_2",
            "has_email_1",
            "has_email_2",
            "has_dni",
            "has_url",
            "has_biography",
            "has_open_to_work",
            "has_vehicle",
            "has_disability",
            "has_disability_percentage",
            "has_incorporation",
            "has_sector",
            "has_category",
            "has_work_experiences",
            "has_hard_skills",
            "has_soft_skills",
            "has_languages",
            "has_academic_educations",
            "has_volunteerings",
            "has_projects",
            "has_publications",
            "has_recognitions_awards",
            "has_certifications_courses",
        ]
        widgets = {
            'urlCV': ReadOnlyWidget(),
            'has_img_profile': ToggleButtonWidget(),
            'has_address': ToggleButtonWidget(),
            'has_phone_1': ToggleButtonWidget(),
            'has_phone_2': ToggleButtonWidget(),
            'has_email_1': ToggleButtonWidget(),
            'has_email_2': ToggleButtonWidget(),
            'has_dni': ToggleButtonWidget(),
            'has_url': ToggleButtonWidget(),
            'has_biography': ToggleButtonWidget(),
            'has_open_to_work': ToggleButtonWidget(),
            'has_vehicle': ToggleButtonWidget(),
            'has_disability': ToggleButtonWidget(),
            'has_disability_percentage': ToggleButtonWidget(),
            'has_incorporation': ToggleButtonWidget(),
            'has_sector': ToggleButtonWidget(),
            'has_category': ToggleButtonWidget(),
            'has_work_experiences': ToggleButtonWidget(),
            'has_hard_skills': ToggleButtonWidget(),
            'has_soft_skills': ToggleButtonWidget(),
            'has_languages': ToggleButtonWidget(),
            'has_academic_educations': ToggleButtonWidget(),
            'has_volunteerings': ToggleButtonWidget(),
            'has_projects': ToggleButtonWidget(),
            'has_publications': ToggleButtonWidget(),
            'has_recognitions_awards': ToggleButtonWidget(),
            'has_certifications_courses': ToggleButtonWidget(),
        }