# Generated by Django 4.0.3 on 2022-04-03 02:11

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, max_length=300, verbose_name='name')),
                ('contact_number', models.CharField(blank=True, max_length=16, verbose_name='contact number')),
                ('roll_number', models.CharField(blank=True, max_length=20, verbose_name='roll number')),
                ('room_number', models.CharField(blank=True, max_length=10, verbose_name='room number')),
                ('usertype', models.CharField(choices=[('STUDENT', 'Student'), ('ELECTRICIAN', 'Electrician'), ('CARPENTER', 'Carpenter'), ('CLEANER', 'Cleaner'), ('PLUMBER', 'Plumber'), ('OTHERS', 'Others')], default='STUDENT', max_length=12, verbose_name='user type')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.user',),
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.user',),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('ELECTRICIAN', 'Electrician'), ('CARPENTER', 'Carpenter'), ('CLEANER', 'Cleaner'), ('PLUMBER', 'Plumber'), ('OTHERS', 'Others')], max_length=100, verbose_name='type')),
                ('description', models.TextField(verbose_name='description')),
                ('date_lodged', models.DateTimeField(auto_now_add=True, verbose_name='date logged')),
                ('mark_done', models.BooleanField(default=False, verbose_name='done by student')),
                ('roll_number', models.CharField(blank=True, default='', max_length=20, verbose_name='roll number')),
                ('room_number', models.CharField(blank=True, default='', max_length=10, verbose_name='room number')),
                ('contact_number', models.CharField(blank=True, max_length=16, verbose_name='contact number')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='main.student')),
            ],
            options={
                'ordering': ['-date_lodged'],
            },
        ),
    ]
