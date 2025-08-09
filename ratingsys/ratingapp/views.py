from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Lecturer, Module, Student, Result, ModuleRating
from .forms import StudentForm, ResultForm, ModuleRatingForm, StudentCSVUploadForm
from django.contrib.auth.decorators import login_required
import csv
from io import TextIOWrapper
from django.contrib import messages

# Dashboard
@login_required
def index(request):
    lecturer = get_object_or_404(Lecturer, user=request.user)
    modules = Module.objects.filter(lecturer=lecturer)

    selected_module_id = request.GET.get("module_id") or request.POST.get("module_id")
    selected_module = None
    enrolled_students = []

    if selected_module_id:
        selected_module = get_object_or_404(Module, id=selected_module_id, lecturer=lecturer)
        
        # Get all students enrolled in this module
        enrolled_students = Student.objects.filter(result__module=selected_module).distinct()

        # Attach .result to each student (None if not existing)
        for student in enrolled_students:
            try:
                student.result = Result.objects.get(student=student, module=selected_module)
            except Result.DoesNotExist:
                student.result = None

        # Handle marks saving
        if request.method == "POST":
            for student in enrolled_students:
                semester_mark = request.POST.get(f"semester_mark_{student.id}")
                exam_mark = request.POST.get(f"exam_mark_{student.id}")
                re_exam_mark = request.POST.get(f"re_exam_mark_{student.id}")

                # Only save if at least one mark is entered
                if semester_mark or exam_mark or re_exam_mark:
                    result, created = Result.objects.get_or_create(
                        student=student,
                        module=selected_module
                    )
                    if semester_mark != "":
                        result.semester_mark = semester_mark
                    if exam_mark != "":
                        result.exam_mark = exam_mark
                    if re_exam_mark != "":
                        result.re_exam_mark = re_exam_mark
                    result.save()

            return redirect(f"{request.path}?module_id={selected_module.id}")

    return render(request, "ratingapp/index.html", {
        "lecturer": lecturer,
        "modules": modules,
        "selected_module_id": str(selected_module_id) if selected_module_id else "",
        "selected_module": selected_module,
        "enrolled_students": enrolled_students
    })


# Add student manually or via CSV
@login_required
def add_student_view(request):
    lecturer = get_object_or_404(Lecturer, user=request.user)

    if request.method == 'POST':
        # MANUAL student form
        if 'manual_submit' in request.POST:
            student_form = StudentForm(request.POST)
            student_form.fields['modules'].queryset = Module.objects.filter(lecturer=lecturer)
            csv_form = StudentCSVUploadForm(lecturer=lecturer)  # empty CSV form

            if student_form.is_valid():
                student = student_form.save()
                modules = student_form.cleaned_data['modules']
                for module in modules:
                    Result.objects.get_or_create(
                        student=student,
                        module=module,
                        defaults={'semester_mark': None, 'exam_mark': None}
                    )

                messages.success(request, "Student added successfully (no marks yet).")
                return redirect('add_student')

        # CSV upload form
        elif 'csv_submit' in request.POST:
            student_form = StudentForm()  # empty manual form
            csv_form = StudentCSVUploadForm(request.POST, request.FILES, lecturer=lecturer)

            if csv_form.is_valid():
                module = csv_form.cleaned_data['module']
                csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
                reader = csv.DictReader(csv_file)

                for row in reader:
                    student, created = Student.objects.get_or_create(
                        student_id=row['student_id'],
                        defaults={'name': row['name'], 'surname': row['surname']}
                    )

                    # Always create Result entry with no marks
                    Result.objects.get_or_create(
                        student=student,
                        module=module,
                        defaults={'semester_mark': None, 'exam_mark': None}
                    )

                messages.success(request, "CSV uploaded: students enrolled without marks.")
                return redirect('add_student')

    else:
        student_form = StudentForm()
        student_form.fields['modules'].queryset = Module.objects.filter(lecturer=lecturer)
        csv_form = StudentCSVUploadForm(lecturer=lecturer)

    return render(request, 'ratingapp/add_student.html', {
        'student_form': student_form,
        'csv_form': csv_form
    })


# Add results later
def add_result_view(request):
    try:
        lecturer = Lecturer.objects.get(user=request.user)
    except Lecturer.DoesNotExist:
        return HttpResponse("You are not linked to any Lecturer account.", status=403)

    result_form = ResultForm(request.POST or None)
    rating_form = ModuleRatingForm(request.POST or None)

    result_form.fields['module'].queryset = Module.objects.filter(lecturer=lecturer)

    if request.method == 'POST':
        if result_form.is_valid() and rating_form.is_valid():
            result = result_form.save()
            rating = rating_form.save(commit=False)
            rating.result = result
            rating.save()
            return redirect('add_result')
    else:
        result_form = ResultForm()
        result_form.fields['module'].queryset = Module.objects.filter(lecturer=lecturer)
        rating_form = ModuleRatingForm()

    return render(request, 'ratingapp/add_result.html', {
        'result_form': result_form,
        'rating_form': rating_form
    })
