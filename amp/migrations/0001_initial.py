# Generated by Django 2.1.5 on 2019-01-21 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('background_check', models.FileField(blank=True, help_text='This field is not required.', null=True, upload_to='background')),
                ('last_background_check_date', models.DateField(blank=True, help_text='This field is not required. Ex. 2012-05-13', null=True)),
                ('last_training_date', models.DateField(blank=True, help_text='This is field is not required. Ex. 2012-05-13', null=True)),
                ('employer', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContractorDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='contractor-documents')),
                ('contractor', models.ForeignKey(help_text='Which contractor does this file reference?', on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='amp.Contractor')),
            ],
        ),
        migrations.CreateModel(
            name='ContractorRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hr_status', models.NullBooleanField()),
                ('tc_status', models.NullBooleanField()),
                ('ace_status', models.NullBooleanField()),
                ('cip_status', models.NullBooleanField()),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('employer', models.CharField(max_length=80)),
                ('remote', models.BooleanField(help_text='Will you be accessing remotely?')),
                ('background_check', models.FileField(blank=True, null=True, upload_to='background')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('background_check', models.FileField(blank=True, help_text='This field is not required.', null=True, upload_to='background')),
                ('last_background_check_date', models.DateField(blank=True, help_text='This field is not required. Ex. 2012-05-13', null=True)),
                ('last_training_date', models.DateField(blank=True, help_text='This is field is not required. Ex. 2012-05-13', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='employee-documents')),
                ('employee', models.ForeignKey(help_text='Which employee does this file reference?', on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='amp.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hr_status', models.NullBooleanField()),
                ('tc_status', models.NullBooleanField()),
                ('ace_status', models.NullBooleanField()),
                ('cip_status', models.NullBooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amp.Employee')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Approval', 'Approval'), ('Rejection', 'Rejection'), ('New Employee', 'New Employee'), ('New Contractor', 'New Contractor'), ('Permission Change', 'Permission Change'), ('New Employee Permission Request', 'New Employee Permission Request'), ('New Contractor Permission Request', 'New Contractor Permission Request')], max_length=160)),
                ('author', models.CharField(max_length=160)),
                ('accessor', models.CharField(max_length=160)),
                ('description', models.TextField()),
                ('creation_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, choices=[('CIP Manager', 'CIP Manager'), ('Alternate CIP Manager', 'Alternate CIP Manager'), ('Access Control Engineer', 'Access Control Engineer'), ('Training Coordinator', 'Training Coordinator'), ('Human Resources', 'Human Resources')], max_length=80, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='amp_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='employeerequest',
            name='permissions',
            field=models.ManyToManyField(related_name='employeerequest_requests', to='amp.Permission'),
        ),
        migrations.AddField(
            model_name='employee',
            name='permissions',
            field=models.ManyToManyField(related_name='employees', to='amp.Permission'),
        ),
        migrations.AddField(
            model_name='contractorrequest',
            name='permissions',
            field=models.ManyToManyField(related_name='contractorrequest_requests', to='amp.Permission'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='permissions',
            field=models.ManyToManyField(related_name='contractors', to='amp.Permission'),
        ),
    ]
