# from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin
# from import_export import resources
# from import_export.fields import Field
# from import_export.widgets import ForeignKeyWidget
# from .models import Student, Result, Marks, ResultResource, StudentResource, MarksResource
#
# @admin.register(Student)
# class StudentAdmin(ImportExportModelAdmin):
#     resource_class = StudentResource
#     list_display = ['id', 'roll_number', 'enrollment_number', 'name', 'father_name', 'dob']
#     search_fields = ['id', 'roll_number', 'enrollment_number', 'name', 'father_name']
#
# @admin.register(Result)
# class ResultAdmin(ImportExportModelAdmin):
#     resource_class = ResultResource
#     list_display = ['id', 'student', 'course', 'semester', 'year', 'title', 'max_marks', 'obtained_marks', 'percentage', 'result_status']
#     search_fields = ['id', 'student__name', 'student__roll_number', 'student__enrollment_number', 'course', 'semester', 'year', 'title']
#
# @admin.register(Marks)
# class MarksAdmin(ImportExportModelAdmin):
#     resource_class = MarksResource
#     list_display = ['id', 'result', 'subject_code', 'subject_name', 'internal_theory_mm', 'internal_theory_mo', 'internal_prac_mm', 'internal_prac_mo', 'external_theory_mm', 'external_theory_mo', 'external_prac_mm', 'external_prac_mo', 'remark']
#     search_fields = ['id', 'result__student__name', 'result__student__roll_number', 'result__student__enrollment_number', 'result__course', 'result__semester', 'result__year', 'subject_code', 'subject_name']
