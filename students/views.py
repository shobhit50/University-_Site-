import base64

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response

from .forms import StudentRegistrationForm, StudentEnrollmentForm, AdmitCardForm
from .serializers import RegistrationSerializer, ExtRegistrationSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView

from .models import Registration, PersonalDetails, Student, Course, Session, Enrollment, AdmitCard, CourseSubject, \
    ContactUs


def index(request):
    return HttpResponse("return this string")

def get_links(request):
    link = RegistrationLink.generate_link()
    print(link)
    return HttpResponse(link)





from django.utils import timezone
from .models import RegistrationLink

@staff_member_required(login_url='admin:login')
def registration_link(request):
    if not request.user.is_staff:
        return redirect('admin:login')
    RegistrationLink.remove_expired()

    if request.method == 'POST':
        num_links = int(request.POST.get('num_links', 1))


        # Generate new links
        links = RegistrationLink.generate_registration_links(num_links)

    # Fetch unused and non-expired links
    unused_links = RegistrationLink.objects.filter(used=False, expiry_date__gt=timezone.now()).order_by('-expiry_date')
    base_address = request.get_host()
    for link in unused_links:
        link.reg_link = base_address + link.reg_link
    context = {
        'links': unused_links
    }

    return render(request, 'registration_link.html', context)


def registration_success(request):
    return render(request, 'registration_success.html')

def student_register(request):
    token = request.GET.get('token')

    try:
        link = RegistrationLink.objects.get(token=token, used=False, expiry_date__gt=timezone.now())
    except RegistrationLink.DoesNotExist:
        return HttpResponse("Invalid link, please contact Admin, and ask for a registration link.")

    # Handle form submission
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the student information and mark the link as used
            Registration.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                gender=form.cleaned_data['gender'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                father_name=form.cleaned_data['father_name'],
                mother_name=form.cleaned_data['mother_name'],
                alternate_mobile=form.cleaned_data['alternate_mobile'],
                aadhar_number=form.cleaned_data['aadhar_number'],
                address=form.cleaned_data['address'],
                state=form.cleaned_data['state'],
                country=form.cleaned_data['country'],
                pincode=form.cleaned_data['pincode'],
                course=form.cleaned_data['course'],
                session=form.cleaned_data['session'],
                photo=form.cleaned_data['photo'].read(),
                signature=form.cleaned_data['signature'].read()
            )

            link.used = True
            link.save()
            return redirect('registration_success')
        else:
            print(form.errors)
    else:
        form = StudentRegistrationForm()

    return render(request, 'student_registration_form.html', {'form': form})


class EnrollmentApprovalView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        # pending_registrations = Registration.objects.defer('photo', 'signature').order_by('-created_at')

        pending_registrations = Registration.objects.defer('photo', 'signature').order_by('-created_at')

        # Registration.objects.filter(approved=True)
        serializer = ExtRegistrationSerializer(pending_registrations, many=True)
        print(serializer.data)
        return render(request, 'pending_registrations.html', {'registrations': serializer.data})

    @transaction.atomic()
    def post(self, request, format=None):
        registration_id = int(request.data.get('registration_id'))

        registration = get_object_or_404(Registration, id=registration_id, approved=False)

        personal_details = PersonalDetails.objects.create(
            full_name=registration.full_name,
            father_name=registration.father_name,
            date_of_birth=registration.date_of_birth,
            gender=registration.gender,
            address=registration.address,
            state=registration.state,
            zip_code=registration.pincode,
            aadhar_number=registration.aadhar_number,
            photo=registration.photo,
            signature=registration.signature
        )
        student = Student.objects.create(
            personal_details=personal_details,
            primary_email=registration.email,
            primary_phone_number=registration.phone_number,
            alternate_phone_number=registration.alternate_mobile
        )

        course = Course.objects.get(course_id=registration.course)
        session_start_year = registration.session.strip()[:4]
        session = Session.objects.get(start_year= session_start_year)

        enrollment = Enrollment.objects.create(
            student=student,
            course=course,
            session=session
        )

        registration.approved = True
        registration.delete()

        # Create success message with enrollment number and roll number
        message = f"Enrollment successful. Enrollment number: {enrollment.enrollment_number}, Roll number: {enrollment.roll_number}"
        # Return JSON response
        return JsonResponse({'message': message})


class GetRegistrationDetailsView(APIView):
    def get(self, request):
        registration_id = request.query_params.get('registration_id')
        if not registration_id:
            return Response({'error': 'registration_id is required'}, status=400)
        try:
            registration = Registration.objects.get(id=registration_id)
            # Encode the photo and signature to base64
            photo = base64.b64encode(registration.photo).decode('utf-8')
            signature = base64.b64encode(registration.signature).decode('utf-8')
            # Add the encoded data to the serialized data
            serializer = ExtRegistrationSerializer(registration)
            serializer_data = serializer.data
            serializer_data['photo'] =  'data:image/jpeg;base64,' +photo
            serializer_data['signature'] =  'data:image/jpeg;base64,' +signature
            return Response(serializer_data)
        except Registration.DoesNotExist:
            return Response({'error': f'Registration with id {registration_id} does not exist'}, status=404)


def enrollment_details(request):
    if request.method == 'POST':
        form = StudentEnrollmentForm(request.POST)
        if form.is_valid():
            results = form.search()
            print(results)
            if results:
                print(results)
                print( results['personal_details'].full_name)
                return render(request, 'enrollment_details.html', {'student': results})
            else:
                form.add_error(None, 'No data found for the given enrollment ID and date of birth.')
    else:
        form = StudentEnrollmentForm()
    return render(request, 'enrollment_details.html', {'form': form})

def get_admit_card(request):
    result_error = 'Result Not Found'
    if request.method == 'GET':
        return admit_form(request)

    form = AdmitCardForm(request.POST)
    if form.is_valid():
        # Get enrollment number and roll number from form
        enrollment_number = form.cleaned_data['enrollment_number']
        roll_number = form.cleaned_data['roll_number']
        year_or_semester = form.cleaned_data['year_or_semester']
        exam_year = form.cleaned_data['exam_year']

        # Get enrollment object for the given enrollment number and roll number
        try:
            enrollment = Enrollment.objects.get(enrollment_number=enrollment_number, roll_number=roll_number)
        except Enrollment.DoesNotExist:
            form.add_error(None, "Enrollment number or roll number is invalid")
            return render(request, 'admit.html',
                          {'form': form, 'error_message': 'Enrollment number or roll number is invalid', 'isAdmitForm': True})

        # Get admit card object for the given enrollment
        try:
            admit_card = AdmitCard.objects.get(student=enrollment.student,year_or_semester = year_or_semester, exam_year = exam_year )
        except AdmitCard.DoesNotExist:
            form.add_error(None, "Admit card is not available for this enrollment")
            return render(request, 'admit.html',
                          {'form': form, 'error_message': 'Admit card is not available for this enrollment', 'isAdmitForm': True})

        # Encode images in personal details of student
        admit_card.student.personal_details.encode_images()

        # Get subjects for the given course and year/semester
        course = admit_card.course
        year_or_semester = admit_card.year_or_semester
        subjects = CourseSubject.objects.filter(course=course, year_or_semester=year_or_semester)

        context = {'admit_card': admit_card, 'subjects': subjects, 'enrollment': enrollment}
        return render(request, 'admit.html', context)
    else:
        form = AdmitCardForm()
    context = {'form': form}
    return render(request, 'admit.html', context)

    # admit_card = AdmitCard.objects.get()
    # admit_card.student.personal_details.encode_images()
    # context = {'admit_card': admit_card}
    # course = admit_card.course
    # year_or_semester = admit_card.year_or_semester
    #
    # subjects = CourseSubject.objects.filter(course=course, year_or_semester=year_or_semester)
    #
    # for subject in subjects:
    #     print(subject.subject)
    # context['subjects'] = subjects
    # print(context)
    # return render(request, 'admit.html', context)

def admit_form(request):
    if request.method == 'POST':
        form = AdmitCardForm(request.POST)
        if form.is_valid():
            # do something with the form data, for example save it to the database
            # ...
            return redirect('get_admit_card')
    else:
        form = AdmitCardForm()
    return render(request, 'admit.html', {'form': form, 'isAdmitForm': True})

def courses(request, cid):
    # Define a dictionary that maps course IDs to template names
    course_templates = {
        1: 'it_and_engineering.html',
        2: 'commerce_and_management.html',
        3: 'social_science_and_humanity.html',
        4: 'science_and_allied_science.html',
        5: 'law.html',
        6: 'agriculture.html',
        7: 'yoga_and_naturopathy.html',
        8: 'research.html',
    }

    # Look up the appropriate template name based on the `cid` parameter
    template_name = course_templates.get(cid)

    # Render the template with the corresponding name, or a default template if `cid` is not valid
    if template_name:
        return render(request, 'courses.html', {'course_html': 'courses/'+template_name})
    else:
        return render(request, 'index.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        ContactUs.objects.create(name=name, phone=phone, email=email, subject=subject, message=message)
    return render(request, 'contact-us.html')
