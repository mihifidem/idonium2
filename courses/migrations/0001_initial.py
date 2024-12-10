# Generated by Django 3.2.12 on 2024-12-10 10:24

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile_cv', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_member', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses_images/')),
                ('is_free', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.category')),
                ('hardskills', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.hardskill')),
            ],
        ),
        migrations.CreateModel(
            name='CourseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('certified', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_users', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_member', models.BooleanField(default=False)),
                ('duration', models.IntegerField(blank=True, default=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('downloadable', models.BooleanField(default=False)),
                ('is_member', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='resources_images/')),
                ('link', models.CharField(blank=True, max_length=50, null=True)),
                ('document', models.FileField(blank=True, null=True, upload_to='')),
                ('is_active', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=False)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.00'), max_digits=10, null=True)),
                ('lesson', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resources', to='courses.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishListType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='WishListUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_wish', models.IntegerField()),
                ('type_wish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.wishlisttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comment', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.course')),
                ('resource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.resource')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='teachers_images/')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile_cv.category')),
                ('hardskills', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile_cv.hardskill')),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile_cv.sector')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='LessonCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('course_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons_completed', to='courses.courseuser')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_completed_lessons', to='courses.lesson')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='courses.module'),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.status'),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='profile_teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.profileteacher'),
        ),
        migrations.AddField(
            model_name='course',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profile_cv.sector'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('ext_certificate', models.FileField(blank=True, null=True, upload_to='')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to='courses.course')),
            ],
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('course__isnull', False), ('resource__isnull', True)), models.Q(('course__isnull', True), ('resource__isnull', False)), _connector='OR'), name='review_course_or_resource_not_both'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='unique_user_course_review'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('user', 'resource'), name='unique_user_resource_review'),
        ),
        migrations.AddConstraint(
            model_name='courseuser',
            constraint=models.UniqueConstraint(fields=('user', 'course'), name='unique_user_course'),
        ),
    ]
