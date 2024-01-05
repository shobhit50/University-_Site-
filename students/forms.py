from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from students.models import Registration, Course, Session, Enrollment, PersonalDetails, AdmitCard


class StudentRegistrationForm(forms.Form):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    # Application Details
    course = forms.ChoiceField(label="Course", required=True)
    session = forms.ChoiceField(required=True)

    # Personal Details
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    alternate_mobile = forms.CharField(max_length=20, required=True)
    father_name = forms.CharField(max_length=100, required=True)
    mother_name = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    aadhar_number = forms.CharField(max_length=20, required=True)
    photo = forms.ImageField(label='Upload Photo', required=True, widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'max_size': 200000}))
    signature = forms.ImageField(label='Upload Signature', required=True, widget=forms.ClearableFileInput(attrs={'accept': 'image/*', 'max_size': 100000}))

    # Address
    address = forms.CharField(max_length=200, required=True)
    pincode = forms.CharField(max_length=10, required=True)
    state   = forms.CharField(max_length=50, required=True)
    country = forms.CharField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].empty_label = 'Select Course'
        self.fields['course'].choices = [(course.course_id, course.course_name) for course in Course.objects.all()]
        # self.fields['session'].choices = [(session.start_year, str(session.start_year) + '-' + str(session.end_year)[2:] ) for session in Session.objects.all()]

        choices_dict = {}
        for session in Session.objects.all():
            key = session.start_year
            value = str(session.start_year) + '-' + str(session.end_year)[2:]
            if key not in choices_dict:
                choices_dict[key] = value
        choices = [(key, value) for key, value in choices_dict.items()]
        self.fields['session'].choices = choices


    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and photo.size > 200 * 1024:
            raise ValidationError("Please keep file size under 200KB.")
        return photo

    def clean_signature(self):
        signature = self.cleaned_data.get('signature')
        if signature and signature.size > 100 * 1024:
            raise ValidationError("Please keep file size under 100KB.")
        return signature


class StudentEnrollmentForm(forms.Form):
    enrollment_id = forms.CharField(label='Enrollment ID', max_length=10,required=True)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    def search(self):
        results = {}
        query1 = self.cleaned_data['enrollment_id']
        query2 = self.cleaned_data['date_of_birth']
        try:
            enrollment_result = Enrollment.objects.get(enrollment_number=query1)
            results['enrollment'] = enrollment_result
            print(type(enrollment_result))

        except Enrollment.DoesNotExist:
            return None
        personal_details_result = enrollment_result.student.personal_details
        enrollment_result.student.personal_details.encode_images()
        results['personal_details'] = personal_details_result
        results['student'] = enrollment_result.student
        results['session'] = enrollment_result.session.get_session()
        print(type(personal_details_result))

        if personal_details_result is None:
            return None

        return results


class AdmitCardForm(forms.ModelForm):
    enrollment_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    roll_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),
    #                                 empty_label=None, to_field_name='course_id', label='Course')
    class Meta:
        model = AdmitCard
        fields = [ 'course', 'year_or_semester', 'exam_year']
        widgets = {
            'exam_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'year_or_semester': forms.NumberInput(attrs={'class': 'form-control'})
        }

    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'




