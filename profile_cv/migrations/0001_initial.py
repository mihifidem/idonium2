# Generated by Django 3.2.12 on 2024-12-12 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('academy_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('current_education', models.BooleanField(blank=True, null=True)),
                ('references', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.category')),
            ],
        ),
        migrations.CreateModel(
            name='FAQResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_key', models.CharField(max_length=100)),
                ('response', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HardSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_hard_skill', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HardSkillUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('level_skill', models.PositiveIntegerField(choices=[(1, '1'), (1, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('hard_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.hardskill')),
            ],
        ),
        migrations.CreateModel(
            name='Incorporation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_incorporation', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IncorporationUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incorporation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.incorporation')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_language', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LanguageUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certifications', models.TextField(blank=True, null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.language')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_level', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Profile_CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_profile', models.ImageField(blank=True, upload_to='profile_images/')),
                ('address', models.CharField(max_length=255)),
                ('phone_1', models.CharField(max_length=20)),
                ('phone_2', models.CharField(max_length=20)),
                ('email_1', models.EmailField(max_length=254)),
                ('email_2', models.EmailField(blank=True, max_length=254, null=True)),
                ('dni', models.CharField(max_length=20, unique=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('open_to_work', models.BooleanField(blank=True, null=True)),
                ('vehicle', models.BooleanField(null=True)),
                ('disability', models.BooleanField(blank=True, null=True)),
                ('disability_percentage', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doi', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('role', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
            ],
        ),
        migrations.CreateModel(
            name='RecognitionAward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('entity', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_sector', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.category')),
            ],
        ),
        migrations.CreateModel(
            name='SectorUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.sector')),
            ],
        ),
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_soft_skill', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SoftSkillUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
                ('soft_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.softskill')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User_cv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlCV', models.CharField(max_length=255, unique=True)),
                ('has_img_profile', models.BooleanField(blank=True, null=True)),
                ('has_address', models.BooleanField(blank=True, null=True)),
                ('has_phone_1', models.BooleanField(blank=True, null=True)),
                ('has_phone_2', models.BooleanField(blank=True, null=True)),
                ('has_email_1', models.BooleanField(blank=True, null=True)),
                ('has_email_2', models.BooleanField(blank=True, null=True)),
                ('has_url', models.BooleanField(blank=True, null=True)),
                ('has_biography', models.BooleanField(blank=True, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('has_open_to_work', models.BooleanField(blank=True, null=True)),
                ('has_vehicle', models.BooleanField(null=True)),
                ('has_disability', models.BooleanField(blank=True, null=True)),
                ('has_disability_percentage', models.BooleanField(blank=True, null=True)),
                ('has_incorporation', models.BooleanField(blank=True, null=True)),
                ('has_sector', models.BooleanField(blank=True, null=True)),
                ('has_category', models.BooleanField(blank=True, null=True)),
                ('has_work_experiences', models.BooleanField(blank=True, null=True)),
                ('has_hard_skills', models.BooleanField(blank=True, null=True)),
                ('has_soft_skills', models.BooleanField(blank=True, null=True)),
                ('has_languages', models.BooleanField(blank=True, null=True)),
                ('has_academic_educations', models.BooleanField(blank=True, null=True)),
                ('has_volunteerings', models.BooleanField(blank=True, null=True)),
                ('has_projects', models.BooleanField(blank=True, null=True)),
                ('has_publications', models.BooleanField(blank=True, null=True)),
                ('has_recognitions_awards', models.BooleanField(blank=True, null=True)),
                ('has_certifications_courses', models.BooleanField(blank=True, null=True)),
                ('profile_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('current_job', models.BooleanField(blank=True, null=True)),
                ('company_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('references', models.TextField(blank=True, null=True)),
                ('hard_skills', models.ManyToManyField(blank=True, to='profile_cv.HardSkillUser')),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteering',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volunteering_position', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('current_volunteering', models.BooleanField(blank=True, null=True)),
                ('entity_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('references', models.TextField(blank=True, null=True)),
                ('profile_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv')),
            ],
        ),
        migrations.CreateModel(
            name='UserCvRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_education', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.academiceducation')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.categoryuser')),
                ('hard_skill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.hardskilluser')),
                ('incorporation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.incorporationuser')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.languageuser')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.project')),
                ('publication', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.publication')),
                ('recognition_award', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.recognitionaward')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.sectoruser')),
                ('soft_skill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.softskilluser')),
                ('user_cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.user_cv')),
                ('volunteering', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.volunteering')),
                ('work_experience', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.workexperience')),
            ],
        ),
        migrations.AddField(
            model_name='user_cv',
            name='relations',
            field=models.ManyToManyField(blank=True, related_name='user_cvs', to='profile_cv.UserCvRelation'),
        ),
        migrations.AddField(
            model_name='user_cv',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.template'),
        ),
        migrations.AddField(
            model_name='languageuser',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.level'),
        ),
        migrations.AddField(
            model_name='languageuser',
            name='profile_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv'),
        ),
        migrations.AddField(
            model_name='incorporationuser',
            name='profile_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv'),
        ),
        migrations.AddField(
            model_name='hardskilluser',
            name='profile_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv'),
        ),
        migrations.AddField(
            model_name='categoryuser',
            name='profile_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv'),
        ),
        migrations.AddField(
            model_name='academiceducation',
            name='profile_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile_cv.profile_cv'),
        ),
    ]
