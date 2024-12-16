from django.db import models
from django.contrib.auth.models import User


# Create Models Here

class Test(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tests")
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_from_json = models.BooleanField(default=False)

class QuestionType(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    content = models.TextField()
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    options = models.JSONField()
    correct_answer = models.CharField(max_length=200)
class Answer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default="default")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, default="default")    
    selected_answer =  models.ForeignKey(Answer, on_delete=models.CASCADE, default="default") 
    is_correct = models.BooleanField(default=False)
    #relacionar hard skills con user test

class UserTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)

class CatergoryType(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Catergory(models.Model):
    name = models.CharField(max_length=200) 
    type = models.ForeignKey(CatergoryType, on_delete=models.CASCADE)

class TestResult(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_test_results")
    duration = models.FloatField(help_text="Duration in minutes")
    is_from_json = models.BooleanField(default=False)
    result = models.FloatField(help_text="Result of the test")
    
    def _str_(self):
        return self.name 

class TestResult(models.Model):
    title = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_test_results")
    duration = models.FloatField(help_text="Duration in minutes")
    is_from_json = models.BooleanField(default=False)
    result = models.FloatField(help_text="Result of the test")
    
    def str(self):
        return self.name

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_management_chatmessages')
    message = models.TextField()
    is_bot = models.BooleanField(default=False)  # True if the message is from the bot, False if from the user
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Message from {'Bot' if self.is_bot else 'User'} at {self.timestamp}"