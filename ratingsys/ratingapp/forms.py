from django import forms
from .models import Student, Result, ModuleRating,Module

class StudentForm(forms.ModelForm):
    modules = forms.ModelChoiceField(
        queryset=Module.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Modules"
    )
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'surname','modules']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'module', 'semester_mark', 'exam_mark', 're_exam_mark', 'final_mark']

class ModuleRatingForm(forms.ModelForm):
    class Meta:
        model = ModuleRating
        fields = ['result', 'rating']

class StudentCSVUploadForm(forms.Form):
    module = forms.ModelChoiceField(queryset=Module.objects.none())
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        lecturer = kwargs.pop('lecturer', None)
        super().__init__(*args, **kwargs)
        if lecturer:
            self.fields['module'].queryset = Module.objects.filter(lecturer=lecturer)
        else:
            self.fields['module'].queryset = Module.objects.none()