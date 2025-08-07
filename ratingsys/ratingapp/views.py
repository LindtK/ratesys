from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Lecturer, Module, Student, Result, ModuleRating
from .forms import StudentForm, ResultForm, ModuleRatingForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    lecturer = get_object_or_404(Lecturer, user=request.user)  # Get the lecturer associated with the logged-in user
    modules = lecturer.modules.all()  # Get all modules taught by the lecturer
    selected_module = request.GET.get('module_id')
 
    results = None
    if selected_module:
        results = Result.objects.filter(module_id=selected_module).select_related('student', 'rating', 'module')

    return render(request, 'ratingapp/index.html', {
        'lecturer': lecturer,
        'modules': modules,
        'results': results,
        'selected_module': selected_module
    })

def add_student_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student')  # redirect to same page or success page
    else:
        form = StudentForm()
    return render(request, 'ratingapp/add_student.html', {'form': form})

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