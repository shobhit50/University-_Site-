from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from students.models import Enrollment, Marks, Result

from .forms import ResultForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

class AboutView(TemplateView):
    template_name = 'about-us.html'

class NoticeView(TemplateView):
    template_name = 'notice.html'

class ContactView(TemplateView):
    template_name = 'contact-us.html'

def result_view(request):
    result_error = 'Result Not Found'
    if request.method == 'GET':
        return result_form(request)
        
    
    print('-----\n---\n\n')
    context = dict()
    context['errors'] = list()
    roll_no = request.POST['roll_number']
    en_no = request.POST['enrollment_number']
    year = request.POST['year']
    course = request.POST['course']
    semester = request.POST['semester']

    try:
        # Get data from DB
        print(roll_no, en_no)
        enrollment = Enrollment.objects.get(roll_number = roll_no,enrollment_number = en_no )
        res = Result.objects.get(enrollment = enrollment, year = year, course = course, semester = semester)
        marks = Marks.objects.filter(result =res)
    except ObjectDoesNotExist as e:
        form = ResultForm(request.POST)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@', e)
        form.add_error(None, result_error)
        return render(request, 'results.html', {'form': form, 'isResultForm': True})
    print('-----------------------------------------------',enrollment)
    context['enrollment'] = enrollment
    
    context['result'] = res
    for i in marks: print(i.subject.subject.subject_name)
    context['subjects'] = marks
    # context['subject_course'] =
    print(context)
    print('\n\n---\n-----')
    context['isResultForm'] = False
    return render(request, 'results.html',  context )

def result_form(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            # do something with the form data, for example save it to the database
            # ...
            return redirect('results')
    else:
        form = ResultForm()
    return render(request, 'results.html', {'form': form, 'isResultForm': True})



