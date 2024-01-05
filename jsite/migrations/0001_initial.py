# Generated by Django 4.0.4 on 2023-02-03 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=50, unique=True)),
                ('enrollment_number', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('father_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=100)),
                ('semester', models.CharField(max_length=50)),
                ('year', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('max_marks', models.PositiveSmallIntegerField()),
                ('obtained_marks', models.PositiveSmallIntegerField()),
                ('percentage', models.FloatField()),
                ('result_status', models.CharField(max_length=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsite.student')),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_code', models.CharField(max_length=50)),
                ('subject_name', models.CharField(max_length=100)),
                ('internal_theory_mm', models.IntegerField()),
                ('internal_theory_mo', models.IntegerField()),
                ('internal_prac_mm', models.IntegerField()),
                ('internal_prac_mo', models.IntegerField()),
                ('external_theory_mm', models.IntegerField()),
                ('external_theory_mo', models.IntegerField()),
                ('external_prac_mm', models.IntegerField()),
                ('external_prac_mo', models.IntegerField()),
                ('remark', models.CharField(max_length=100)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jsite.result')),
            ],
        ),
    ]
