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


class StudentResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'module', 'semester_mark', 'exam_mark', 're_exam_mark', 'final_mark']

    def __init__(self, *args, **kwargs):
        lecturer = kwargs.pop('lecturer', None)  # Get lecturer from the view
        
        super().__init__(*args, **kwargs)
        if lecturer:
            self.fields['module'].queryset = Module.objects.filter(lecturer=lecturer)
        module_selected = kwargs.pop('module_selected', None)
        
        if module_selected:
            self.fields['student'].queryset = Student.objects.filter(
                modules=module_selected
            )
        else:
            self.fields['student'].queryset = Student.objects.none()

class CSVUploadForm(forms.Form):
    module = forms.ModelChoiceField(queryset=Module.objects.none())
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        lecturer = kwargs.pop('lecturer', None)  # Get lecturer from the view
        super().__init__(*args, **kwargs)
        if lecturer:
            self.fields['module'].queryset = Module.objects.filter(lecturer=lecturer)
