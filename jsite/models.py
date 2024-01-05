from django.db import models
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

class Student(models.Model):
    roll_number = models.CharField(max_length=50, unique=True)
    enrollment_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    dob = models.DateField()

    def __str__(self):
        return self.name

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    max_marks = models.PositiveSmallIntegerField()
    obtained_marks = models.PositiveSmallIntegerField()
    percentage = models.FloatField()
    result_status = models.CharField(max_length=10)

    def __str__(self):
        return f"Result for {self.student} in {self.course}-{self.semester}"

class Marks(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=100)
    internal_theory_mm = models.IntegerField()
    internal_theory_mo = models.IntegerField()
    internal_prac_mm = models.IntegerField()
    internal_prac_mo = models.IntegerField()
    external_theory_mm = models.IntegerField()
    external_theory_mo = models.IntegerField()
    external_prac_mm = models.IntegerField()
    external_prac_mo = models.IntegerField()
    total_mm = models.IntegerField()
    total_mo = models.IntegerField()
    remark = models.CharField(max_length=100)

    def __str__(self):
        return f"Marks for {self.subject_name} in {self.result}"

# Resources for import_export
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ['id', 'roll_number', 'enrollment_number', 'name', 'father_name', 'dob']
        export_order = fields

class ResultResource(resources.ModelResource):
    student = fields.Field(
        column_name='student',
        attribute='student',
        widget=ForeignKeyWidget(Student, 'id')
    )

    class Meta:
        model = Result
        fields = ['id', 'student', 'course', 'semester', 'year', 'title', 'max_marks', 'obtained_marks', 'percentage', 'result_status']
        export_order = fields
        import_id_fields = ['id']


class MarksResource(resources.ModelResource):
    result = fields.Field(
        column_name='result',
        attribute='result',
        widget=ForeignKeyWidget(Result, 'id')
    )

    class Meta:
        model = Marks
        fields = ['id', 'result', 'subject_code', 'subject_name', 'internal_theory_mm', 
        'internal_theory_mo', 'internal_prac_mm', 'internal_prac_mo', 'external_theory_mm', 
        'external_theory_mo','external_prac_mm', 'external_prac_mo',
        'total_mm', 'total_mo', 'remark']
        export_order = fields
        import_id_fields = ['id']