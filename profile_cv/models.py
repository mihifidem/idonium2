from django.db import models
from django.contrib.auth.models import User
from courses.models import *

# Model to represent a user's profile
class Profile_CV(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name='profile_user')  # One-to-one relationship with the User model
    img_profile = models.ImageField(upload_to='profile_images/', blank=True)  # Profile picture
    img_1_profile = models.ImageField(upload_to='profile_images/', blank=True)  # Profile picture
    img_2_profile = models.ImageField(upload_to='profile_images/', blank=True)  # Profile picture
    img_3_profile = models.ImageField(upload_to='profile_images/', blank=True)  # Profile picture
    img_4_profile = models.ImageField(upload_to='profile_images/', blank=True)  # Profile picture
    address = models.CharField(max_length=255)  # User's address
    phone_1 = models.CharField(max_length=20)  # User's phone number
    phone_2 = models.CharField(max_length=20)  # User's phone number
    email_1 = models.EmailField()  # User's primary email
    email_2 = models.EmailField(blank=True, null=True)  # Optional secondary email
    dni = models.CharField(max_length=20, unique=True)  # Unique DNI of the user
    biography = models.TextField(blank=True, null=True)  # Optional biography of the user
    open_to_work = models.BooleanField(blank=True, null=True)
    vehicle = models.BooleanField(blank=False, null=True)
    disability = models.BooleanField(blank=True, null=True)
    disability_percentage = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Model to represent a user's CV
class User_cv(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE, blank=True, null=True)  # One-to-one relationship with the User model
    urlCV = models.URLField(unique=True, blank=True, null=True)  # Optional URL of the user
    template = models.CharField(max_length=255)  # Template of the CV
    has_img_profile = models.BooleanField(blank=True, null=True)  # Profile picture
    has_address =  models.BooleanField(blank=True, null=True)  # User's address
    has_phone_1 = models.BooleanField(blank=True, null=True)# User's phone number
    has_phone_2 = models.BooleanField(blank=True, null=True)# User's phone number
    has_email_1 = models.BooleanField(blank=True, null=True) # User's primary email
    has_email_2 = models.BooleanField(blank=True, null=True) # Optional secondary email
    has_dni = models.BooleanField(blank=True, null=True)  # Unique DNI of the user
    has_url = models.BooleanField(blank=True, null=True)  # Optional URL of the user
    has_biography = models.BooleanField(blank=True, null=True)  # Optional biography of the user
    biography = models.TextField(blank=True, null=True)  # Optional biography of the user
    has_open_to_work = models.BooleanField(blank=True, null=True)
    has_vehicle = models.BooleanField(blank=False, null=True)
    has_disability = models.BooleanField(blank=True, null=True)
    has_disability_percentage = models.BooleanField(blank=True, null=True)
    has_incorporation = models.BooleanField(blank=True, null=True)  # Incorporation
    has_sector = models.BooleanField(blank=True, null=True)  # Sector
    has_category = models.BooleanField(blank=True, null=True)  # Category
    has_work_experiences = models.BooleanField(blank=True, null=True)
    has_hard_skills = models.BooleanField(blank=True, null=True)
    has_soft_skills = models.BooleanField(blank=True, null=True)
    has_languages = models.BooleanField(blank=True, null=True)
    has_academic_educations = models.BooleanField(blank=True, null=True)
    has_volunteerings = models.BooleanField(blank=True, null=True)
    has_projects = models.BooleanField(blank=True, null=True)
    has_publications = models.BooleanField(blank=True, null=True)
    has_recognitions_awards = models.BooleanField(blank=True, null=True)
    has_certifications_courses = models.BooleanField(blank=True, null=True)
    relations = models.ManyToManyField("UserCvRelation", blank=True,  related_name="user_cvs")

    def __str__(self):
        return self.profile_user.user.username

class UserCvRelation(models.Model):
    user_cv = models.ForeignKey('User_cv', on_delete=models.CASCADE)
    work_experience = models.ForeignKey('WorkExperience', on_delete=models.CASCADE, null=True, blank=True)
    academic_education = models.ForeignKey('AcademicEducation', on_delete=models.CASCADE, null=True, blank=True)
    hard_skill = models.ForeignKey('HardSkillUser', on_delete=models.CASCADE, null=True, blank=True)
    soft_skill = models.ForeignKey('SoftSkillUser', on_delete=models.CASCADE, null=True, blank=True)
    language = models.ForeignKey('LanguageUser', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('CategoryUser', on_delete=models.CASCADE, null=True, blank=True)
    sector = models.ForeignKey('SectorUser', on_delete=models.CASCADE, null=True, blank=True)
    incorporation = models.ForeignKey('IncorporationUser', on_delete=models.CASCADE, null=True, blank=True)
    volunteering = models.ForeignKey('Volunteering', on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True, blank=True)
    publication = models.ForeignKey('Publication', on_delete=models.CASCADE, null=True, blank=True)
    recognition_award = models.ForeignKey('RecognitionAward', on_delete=models.CASCADE, null=True, blank=True)

# Model to represent a work experience
class WorkExperience(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    job_title = models.CharField(max_length=255)  # Job title
    start_date = models.DateField()  # Start date
    end_date = models.DateField(blank=True, null=True)  # Optional end date
    current_job = models.BooleanField(blank=True, null=True)  # Current job
    company_name = models.CharField(max_length=255)  # Company name
    description = models.TextField(blank=True, null=True)  # Optional description
    achievements = models.TextField(blank=True, null=True)  # Optional achievements
    references = models.TextField(blank=True, null=True)  # Optional references
    hard_skills = models.ManyToManyField("HardSkillUser", blank=True)  # Hard skills

    def __str__(self):
        return self.job_title

# Model to represent an academic education
class AcademicEducation(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    title = models.CharField(max_length=255)  # Title of the education
    academy_name = models.CharField(max_length=255)  # Name of the academy
    start_date = models.DateField()  # Start date
    end_date = models.DateField(blank=True, null=True)  # Optional end date
    current_education = models.BooleanField(blank=True, null=True)  # Current education
    references = models.TextField(blank=True, null=True)  # Optional references

    def __str__(self):
        return self.title

# Model to represent a hard skill
class HardSkillUser(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    hard_skill = models.ForeignKey("HardSkill", on_delete=models.CASCADE)  # Name of the skill
    description = models.TextField(blank=True, null=True)  # Optional description
    level_skill = models.PositiveIntegerField(choices=((1,'1'),(1,'2'),(3,'3'),(4,'4'),(5,'5'))) # Proficiency level of the skill

    def __str__(self):
        return self.hard_skill.name_hard_skill

# Model to represent a soft skill
class SoftSkillUser(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    soft_skill = models.ForeignKey("SoftSkill", on_delete=models.CASCADE)  # Name of the skill
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.soft_skill.name_soft_skill

# Model to represent a language
class LanguageUser(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    language = models.ForeignKey("Language", on_delete=models.CASCADE)  # Name of the language
    level = models.ForeignKey("Level", on_delete=models.CASCADE)  # Proficiency level of the language
    certifications = models.TextField(blank=True, null=True)  # Optional certifications

    def __str__(self):
        return self.language.name_language

# Model to represent a Category
class CategoryUser(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    category = models.ForeignKey("Category", on_delete=models.CASCADE)  # Name of the category

    def __str__(self):
        return self.category.name_category

# Model to represent a Sector
class SectorUser(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    sector = models.ForeignKey("Sector", on_delete=models.CASCADE)  # Name of the sector

    def __str__(self):
        return self.sector.name_sector

# Model to represent a Incorporation
class IncorporationUser(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    incorporation = models.ForeignKey("Incorporation", on_delete=models.CASCADE)  # Name of the incorporation

    def __str__(self):
        return self.incorporation.name_incorporation

# Model to represent a volunteering
class Volunteering(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    volunteering_position = models.CharField(max_length=255)  # Volunteering position
    start_date = models.DateField()  # Start date
    end_date = models.DateField(blank=True, null=True)  # Optional end date
    current_volunteering = models.BooleanField(blank=True, null=True)  # Current volunteering
    entity_name = models.CharField(max_length=255)  # Name of the entity
    description = models.TextField(blank=True, null=True)  # Optional description
    achievements = models.TextField(blank=True, null=True)  # Optional achievements
    references = models.TextField(blank=True, null=True)  # Optional references

    def __str__(self):
        return self.volunteering_position

# Model to represent a project
class Project(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    name = models.CharField(max_length=255)  # Name of the project
    description = models.TextField()  # Description of the project
    link = models.URLField(blank=True, null=True)  # Optional link to the project

    def __str__(self):
        return self.name

# Model to represent a publication
class Publication(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    doi = models.CharField(max_length=100, blank=True, null=True)  # Optional DOI
    url = models.URLField(blank=True, null=True)  # Optional URL
    role = models.CharField(max_length=255)  # Role in the publication
    name = models.CharField(max_length=255)  # Name of the publication

    def __str__(self):
        return self.doi

# Model to represent a recognition or award
class RecognitionAward(models.Model):
    profile_user = models.ForeignKey(Profile_CV, on_delete=models.CASCADE)  # One-to-one relationship with the User model
    name = models.CharField(max_length=255)  # Name of the recognition or award
    entity = models.CharField(max_length=255)  # Entity that grants the recognition or award
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name
    

class FAQResponse(models.Model):
    question_key = models.CharField(max_length=100)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_key

# Models to represent Enums
class HardSkill (models.Model):
    name_hard_skill = models.CharField(max_length=50)  # Name of the skill

    def __str__(self):
        return self.name_hard_skill

class SoftSkill (models.Model):
    name_soft_skill = models.CharField(max_length=50)  # Name of the skill

    def __str__(self):
        return self.name_soft_skill
class Language (models.Model):
    name_language = models.CharField(max_length=100)  # Name of the language

    def __str__(self):
        return self.name_language
class Category(models.Model):
    name_category = models.CharField(max_length=100)  # Name of the category

    def __str__(self):
        return self.name_category

class Sector(models.Model):
    name_sector = models.CharField(max_length=100)  # Name
    category = models.ForeignKey("Category", on_delete=models.CASCADE)  # Category

    def __str__(self):
        return self.name_sector

class Incorporation(models.Model):
    name_incorporation = models.CharField(max_length=100)  # Name

    def __str__(self):
        return self.name_incorporation

class Level (models.Model):
    name_level = models.CharField(max_length=2)

    def __str__(self):
        return self.name_level