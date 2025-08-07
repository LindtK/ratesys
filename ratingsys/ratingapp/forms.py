from django import forms
from .models import Student, Result, ModuleRating

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'surname']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'module', 'semester_mark', 'exam_mark', 're_exam_mark', 'final_mark']

class ModuleRatingForm(forms.ModelForm):
    class Meta:
        model = ModuleRating
        fields = ['result', 'rating']

