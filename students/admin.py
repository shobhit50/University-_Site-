from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources


from students.models import RegistrationLink, RegistrationLinkResource, Registration, Course, Session, Enrollment, \
    Student, PersonalDetails, Subject, AdmitCard, CourseSubject, Result, Marks, ContactUs

admin.site.site_header = 'Admin - JV University'
admin.site.site_title = "JV Admin"


@admin.register(RegistrationLink)
class RegistrationLinkAdmin(ImportExportModelAdmin):
    resource_class = RegistrationLinkResource
    list_display = ['reg_link', 'expiry_date', 'used']
    search_fields = ['reg_link', 'expiry_date', 'used']


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'aadhar_number', 'gender', 'date_of_birth', 'created_at')



class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'course_description', 'duration_type', 'duration']
        export_order = fields


class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource
    list_display = ['course_id', 'course_name', 'course_description', 'duration_type', 'duration']
    search_fields = ['course_id', 'course_name']


class SessionAdmin(admin.ModelAdmin):
    list_display = ['start_year', 'end_year']
    search_fields = ['start_year', 'end_year']


class EnrollmentResource(resources.ModelResource):
    class Meta:
        model = Enrollment
        fields = ['enrollment_number', 'roll_number', 'student', 'course', 'academic_term', 'enrollment_year', 'enrollment_date']
        export_order = fields


class EnrollmentAdmin(ImportExportModelAdmin):
    resource_class = EnrollmentResource
    list_display = ['enrollment_number', 'roll_number', 'student', 'course', 'enrollment_year', 'enrollment_date', 'session']
    search_fields = ['enrollment_number', 'roll_number', 'student__personal_details__full_name', 'course__course_id', 'enrollment_year']
    list_filter = ['course', 'enrollment_year']


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ['student_id', 'personal_details', 'primary_email', 'primary_phone_number', 'alternate_phone_number']
        export_order = fields


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource
    list_display = ['student_id', 'personal_details', 'primary_email', 'primary_phone_number', 'alternate_phone_number']
    search_fields = ['student_id', 'personal_details', 'primary_email', 'primary_phone_number', 'alternate_phone_number']

class PersonalDetailsResource(resources.ModelResource):
    class Meta:
        model = PersonalDetails
        fields = ['personal_details_id', 'full_name', 'father_name', 'date_of_birth', 'gender', 'address', 'state', 'zip_code', 'aadhar_number']
        export_order = fields

class PersonalDetailsAdmin(ImportExportModelAdmin):
    resource_class = PersonalDetailsResource
    list_display = ['personal_details_id', 'full_name', 'father_name', 'date_of_birth', 'gender', 'address', 'state', 'zip_code', 'aadhar_number']
    search_fields = ['personal_details_id', 'full_name', 'father_name', 'date_of_birth', 'gender', 'address', 'state', 'zip_code', 'aadhar_number']

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ['subject_id', 'subject_name']
        export_order = fields


class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_display = ['subject_id', 'subject_name']
    search_fields = ['subject_id', 'subject_name']


class AdmitCardResource(resources.ModelResource):
    class Meta:
        model = AdmitCard
        fields = ['admit_card_id', 'exam_name', 'student', 'exam_year', 'course', 'year_or_semester']
        export_order = fields


class AdmitCardAdmin(ImportExportModelAdmin):
    resource_class = AdmitCardResource
    list_display = ['admit_card_id', 'exam_name', 'student', 'exam_year', 'year_or_semester']
    search_fields = ['admit_card_id', 'exam_name', 'student__name', 'exam_year', 'year_or_semester']
    list_filter = ['course__course_id', 'year_or_semester']


class CourseSubjectResource(resources.ModelResource):
    class Meta:
        model = CourseSubject
        fields = ['course', 'subject', 'year_or_semester', 'internal_max_marks', 'internal_min_marks', 'external_max_marks', 'external_min_marks']
        export_order = fields


class CourseSubjectAdmin(ImportExportModelAdmin):
    resource_class = CourseSubjectResource
    list_display = ['course', 'subject', 'year_or_semester', 'internal_max_marks', 'internal_min_marks', 'external_max_marks', 'external_min_marks']
    search_fields = ['course__course_id', 'subject__subject_name', 'year_or_semester']
    list_filter = ['course__course_id', 'year_or_semester']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'subject', 'message')


# @admin.register(Result)
# class ResultAdmin(admin.ModelAdmin):
#
#     autocomplete_fields = ['enrollment']

class ResultResource(resources.ModelResource):
    class Meta:
        model = Result
        fields = ['title', 'course', 'year', 'semester', 'enrollment', 'max_marks', 'obtained_marks', 'percentage', 'result_status']
        export_order = fields

class ResultAdmin(ImportExportModelAdmin):
    resource_class = ResultResource
    list_display = ['title', 'course', 'year', 'semester', 'enrollment', 'max_marks', 'obtained_marks', 'percentage', 'result_status']
    search_fields = ['enrollment__student__personal_details__full_name', 'course__course_id', 'semester']
    autocomplete_fields = ['enrollment']

class MarksResource(resources.ModelResource):
    class Meta:
        model = Marks
        fields = ['subject', 'result', 'internal_marks', 'external_marks', 'total_mm', 'total_mo', 'remark']
        export_order = fields

class MarksAdmin(ImportExportModelAdmin):
    resource_class = MarksResource
    list_display = ['subject', 'result', 'internal_marks', 'external_marks', 'total_mm', 'total_mo', 'remark']
    search_fields = ['result__enrollment__student__personal_details__full_name', 'result__course__course_id', 'subject__subject_name']
    autocomplete_fields = ['result', 'subject']

admin.site.register(Marks, MarksAdmin)


admin.site.register(Result, ResultAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)





admin.site.register(ContactUs, ContactUsAdmin)



admin.site.register(Course, CourseAdmin)
admin.site.register(Session, SessionAdmin)
# admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(PersonalDetails, PersonalDetailsAdmin)


admin.site.register(Registration, RegistrationAdmin)

admin.site.register(Subject, SubjectAdmin)
admin.site.register(AdmitCard, AdmitCardAdmin)
admin.site.register(CourseSubject, CourseSubjectAdmin)
# admin.site.register(Result)
# admin.site.register(Marks)
