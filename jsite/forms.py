from django import forms
from students.models import Result

class ResultForm(forms.Form):
    course = forms.ChoiceField(label="Course", required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    semester = forms.ModelChoiceField(queryset=Result.objects.values_list('semester', flat=True).distinct(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    roll_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    enrollment_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.ModelChoiceField(queryset=Result.objects.values_list('year', flat=True).distinct(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['course'].choices = [(course[0], course[1]) for course in Result.objects.values_list('course__course_id','course__course_name').distinct()]
        self.fields['course'].choices.insert(0, ('', '---------'))



