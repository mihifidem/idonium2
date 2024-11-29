import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from profile_cv.models import (
    Profile_CV, User_cv, WorkExperience, AcademicEducation, HardSkillUser, SoftSkillUser, LanguageUser,
    CategoryUser, SectorUser, IncorporationUser, Volunteering, Project, Publication, RecognitionAward,
    HardSkill, SoftSkill, Language, Category, Sector, Incorporation, Level
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

fake = Faker()

def create_fake_data(n):
    for _ in range(n):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='password123'
        )
        
        profile_cv = Profile_CV.objects.create(
            user=user,
            img_profile=fake.image_url(),
            img_1_profile=fake.image_url(),
            img_2_profile=fake.image_url(),
            img_3_profile=fake.image_url(),
            img_4_profile=fake.image_url(),
            address=fake.address(),
            phone_1=fake.phone_number(),
            phone_2=fake.phone_number(),
            email_1=fake.email(),
            email_2=fake.email(),
            dni=fake.unique.ssn(),
            biography=fake.text(),
            open_to_work=fake.boolean(),
            vehicle=fake.boolean(),
            disability=fake.boolean(),
            disability_percentage=random.randint(0, 100) if fake.boolean() else None
        )

        User_cv.objects.create(
            profile_user=profile_cv,
            urlCV=fake.url(),
            template=fake.word(),
            has_img_profile=fake.boolean(),
            has_address=fake.boolean(),
            has_phone_1=fake.boolean(),
            has_phone_2=fake.boolean(),
            has_email_1=fake.boolean(),
            has_email_2=fake.boolean(),
            has_dni=fake.boolean(),
            has_url=fake.boolean(),
            has_biography=fake.boolean(),
            biography=fake.text(),
            has_open_to_work=fake.boolean(),
            has_vehicle=fake.boolean(),
            has_disability=fake.boolean(),
            has_disability_percentage=fake.boolean(),
            has_incorporation=fake.boolean(),
            has_sector=fake.boolean(),
            has_category=fake.boolean(),
            has_work_experiences=fake.boolean(),
            has_hard_skills=fake.boolean(),
            has_soft_skills=fake.boolean(),
            has_languages=fake.boolean(),
            has_academic_educations=fake.boolean(),
            has_volunteerings=fake.boolean(),
            has_projects=fake.boolean(),
            has_publications=fake.boolean(),
            has_recognitions_awards=fake.boolean(),
            has_certifications_courses=fake.boolean()
        )

        for _ in range(random.randint(1, 5)):
            WorkExperience.objects.create(
                profile_user=profile_cv,
                job_title=fake.job(),
                start_date=fake.date(),
                end_date=fake.date(),
                current_job=fake.boolean(),
                company_name=fake.company(),
                description=fake.text(),
                achievements=fake.text(),
                references=fake.text(),
                hard_skills=HardSkillUser.objects.create(
                    profile_user=profile_cv,
                    hard_skill=HardSkill.objects.create(name_hard_skill=fake.word()),
                    description=fake.text(),
                    level_skill=random.randint(1, 5)
                )
            )

        AcademicEducation.objects.create(
            profile_user=profile_cv,
            title=fake.word(),
            academy_name=fake.company(),
            start_date=fake.date(),
            end_date=fake.date(),
            current_education=fake.boolean(),
            references=fake.text()
        )

        HardSkillUser.objects.create(
            profile_user=profile_cv,
            hard_skill=HardSkill.objects.create(name_hard_skill=fake.word()),
            description=fake.text(),
            level_skill=random.randint(1, 5)
        )

        SoftSkillUser.objects.create(
            profile_user=profile_cv,
            soft_skill=SoftSkill.objects.create(name_soft_skill=fake.word()),
            description=fake.text()
        )

        LanguageUser.objects.create(
            profile_user=profile_cv,
            language=Language.objects.create(name_language=fake.word()),
            level=Level.objects.create(name_level=fake.word()),
            certifications=fake.text()
        )

        CategoryUser.objects.create(
            profile_user=profile_cv,
            category=Category.objects.create(name_category=fake.word())
        )

        SectorUser.objects.create(
            profile_user=profile_cv,
            sector=Sector.objects.create(name_sector=fake.word())
        )

        IncorporationUser.objects.create(
            profile_user=profile_cv,
            incorporation=Incorporation.objects.create(name_incorporation=fake.word())
        )

        Volunteering.objects.create(
            profile_user=profile_cv,
            volunteering_position=fake.job(),
            start_date=fake.date(),
            end_date=fake.date(),
            current_volunteering=fake.boolean(),
            entity_name=fake.company(),
            description=fake.text(),
            achievements=fake.text(),
            references=fake.text()
        )

        Project.objects.create(
            profile_user=profile_cv,
            name=fake.word(),
            description=fake.text(),
            link=fake.url()
        )

        Publication.objects.create(
            profile_user=profile_cv,
            doi=fake.word(),
            url=fake.url(),
            role=fake.job(),
            name=fake.word()
        )

        RecognitionAward.objects.create(
            profile_user=profile_cv,
            name=fake.word(),
            entity=fake.company(),
            description=fake.text()
        )

if __name__ == '__main__':
    create_fake_data(10)