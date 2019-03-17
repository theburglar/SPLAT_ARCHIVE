from django.db import models
from django.utils.timezone import now

# Create your models here.

class Student(models.Model):
    username = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    prac = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.username}: {self.name}'

class Assignment(models.Model):
    name = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    criteria = models.TextField()

    def __str__(self):
        return f'{self.name}'

class Submission(models.Model):
    # Foreign Keys
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # Fields
    submission_time = models.DateTimeField(default=now)
    file = models.FileField()
    static_analysis = models.TextField()
    test_results = models.TextField()
    mark_sheet = models.TextField()
    comments = models.TextField()

    def __str__(self):
        return f'{self.assignment} by {self.student} @ {self.submission_time}'