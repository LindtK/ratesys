from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Module(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credits = models.PositiveIntegerField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE,related_name='modules')

    def __str__(self):
        return f"{self.name} ({self.code})"

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    modules = models.ManyToManyField(Module, through='Result')

    def __str__(self):
        return f"{self.name} {self.surname}"

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    semester_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exam_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    re_exam_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    final_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student.name} - {self.module.name} - {self.final_mark}"

class ModuleRating(models.Model):
    result = models.OneToOneField(Result, on_delete=models.CASCADE, related_name='rating')
    RATING_CHOICES = [
        ('FAIL', 'Fail'),
        ('PASS', 'Pass'),
        ('DISTINCTION', 'Pass with Distinction'),
    ]
    rating = models.CharField(max_length=15, choices=RATING_CHOICES)

    def __str__(self):
        return f"{self.result.student} - {self.result.module} - {self.rating}"