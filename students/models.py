import base64
from datetime import datetime

from django.db import models
from django.utils import timezone
import secrets
from import_export import resources, fields
from django.urls import reverse, path
from django.utils.html import format_html
from django.db.models import Q


class RegistrationLink(models.Model):
    reg_link = models.CharField(max_length=250, unique=True)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)
    token = models.CharField(max_length=20, unique=True)

    @classmethod
    def generate_link(cls, expiry_days=7):
        token = secrets.token_hex(4)
        expiry_date = timezone.now() + timezone.timedelta(days=expiry_days)
        reg_link = reverse('student_register') + f'?token={token}'
        link = cls(reg_link=reg_link, expiry_date=expiry_date, token=token)
        link.save()
        return reg_link

    @classmethod
    def remove_expired(cls):
        now = timezone.now()
        cls.objects.filter(Q(expiry_date__lte=now) | Q(used=True)).delete()

    @classmethod
    def generate_registration_links(cls, num_links):
        links = []
        for i in range(num_links):
            link = RegistrationLink.generate_link()
            links.append(link)
        return links


class RegistrationLinkResource(resources.ModelResource):
    class Meta:
        model = RegistrationLink
        fields = ['reg_link', 'expiry_date', 'used']
        export_order = fields


from django.db import models


class Registration(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    alternate_mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    course = models.CharField(max_length=50)
    session = models.CharField(max_length=20)
    photo = models.BinaryField()
    signature = models.BinaryField()
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    aadhar_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)


class PersonalDetails(models.Model):
    personal_details_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    aadhar_number = models.CharField(max_length=20)
    photo = models.BinaryField()
    signature = models.BinaryField()

    def __str__(self):
        return f"{self.full_name}"

    def encode_images(self):
        self.photo = 'data:image/jpeg;base64,' + base64.b64encode(self.photo).decode('utf-8')
        self.signature = 'data:image/jpeg;base64,' + base64.b64encode(self.signature).decode('utf-8')


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE)
    primary_email = models.EmailField()
    primary_phone_number = models.CharField(max_length=20)
    alternate_phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.personal_details.full_name}"


class Course(models.Model):
    DURATION_TYPE_CHOICES = [
        ('year', 'Year'),
        ('semester', 'Semester'),
    ]
    COURSE_TYPE_CHOICES = [
        ('internal', 'internal'),
        ('external', 'external'),
    ]
    course_id = models.CharField(primary_key=True, max_length=6)
    course_name = models.CharField(max_length=100)
    duration_type = models.CharField(max_length=10, choices=DURATION_TYPE_CHOICES)
    course_type = models.CharField(max_length=10, choices=COURSE_TYPE_CHOICES)
    duration = models.IntegerField()
    course_description = models.TextField()

    def __str__(self):
        return f"{self.course_name}"


class Session(models.Model):
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()
    # course = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['start_year', 'end_year']

    def get_session(self):
        return str(self.start_year) + '-' + str(self.end_year % 100)

    def __str__(self):
        return str(self.start_year) + '-' + str(self.end_year % 100)


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    enrollment_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    # academic_term = models.CharField(max_length=20)
    enrollment_year = models.CharField(max_length=4, default=datetime.now().year)
    enrollment_date = models.DateField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.personal_details.full_name + ' - ' + self.enrollment_number}"

    def save(self, *args, **kwargs):
        if not self.enrollment_number:
            current_year = timezone.now().year
            last_enrollment = Enrollment.objects.filter(enrollment_number__startswith='JV'+str(current_year)).order_by(
                '-enrollment_number').first()
            if last_enrollment:
                last_id = int(last_enrollment.enrollment_number[-6:])
                new_id = last_id + 1
            else:
                new_id = 100000
            self.enrollment_number = f"JV{current_year}{new_id}"

        if not self.roll_number:

            session_start_year_short = str(self.session.start_year)[-2:]
            last_roll_number = Enrollment.objects.filter(
                roll_number__startswith=session_start_year_short + self.course.course_id).order_by(
                '-roll_number').first()
            if last_roll_number:
                last_id = int(last_roll_number.roll_number[-4:])
                new_id = last_id + 1
            else:
                new_id = 1
            self.roll_number = f"{session_start_year_short}{self.course.course_id}{new_id:04d}"
        super().save(*args, **kwargs)


class Subject(models.Model):
    subject_id = models.CharField(max_length=10, primary_key=True)
    subject_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subject_name


class AdmitCard(models.Model):
    admit_card_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=255)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_year = models.PositiveSmallIntegerField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    year_or_semester = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.exam_name} Admit Card for {self.student}"


class CourseSubject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year_or_semester = models.IntegerField()
    internal_max_marks = models.IntegerField()
    internal_min_marks = models.IntegerField()
    external_max_marks = models.IntegerField()
    external_min_marks = models.IntegerField()

    def __str__(self):
        return f"{self.course.course_id} - {self.subject.subject_name}"

    class Meta:
        unique_together = ('course', 'subject', 'year_or_semester')


class Result(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE,related_name='results')
    max_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    percentage = models.FloatField()
    result_status = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.enrollment.student.personal_details.full_name + ' - ' + self.course.course_id + ' ' + str(self.semester)}"


class Marks(models.Model):
    subject = models.ForeignKey(CourseSubject, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    internal_marks = models.IntegerField()
    external_marks = models.IntegerField()
    total_mm = models.IntegerField()
    total_mo = models.IntegerField()
    remark = models.CharField(max_length=100, default='PASS')

    def __str__(self):
        return f"{self.subject} - {self.internal_marks} - {self.external_marks}"

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
