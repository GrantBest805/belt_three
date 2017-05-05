from __future__ import unicode_literals
import re, datetime, bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def reg(self, data):
        errors = []
        # start of form data validations
        # first name validation
        if len(data['first_name']) < 2:
            errors.append("First name must be more then two characters.")
        if not data['first_name'].isalpha():
            errors.append("First name must contain only letters.")
        # last name validation
        if len(data['last_name']) < 2:
            errors.append("Last name must be more then two characters.")
        if not data['last_name'].isalpha():
            errors.append("Last name must contain only letters.")
        # email validation
        if data['email'] == "":
            errors.append("Email cannot be blank.")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Please enter a valid email address.")
        # check if email in database
        try:
            User.objects.get(email=data['email'])
            errors.append("Email is already registered.")
        except:
            pass

        # password validation
        if len(data['password']) < 8:
            errors.append("Email must be at least eight characters.")
        if data['password'] != data['confirm']:
            errors.append("Passwords do not match.")
        # DOB validation
        if data['dob'] == '':
            errors.append("Birthday is required.")
        elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
            errors.append("You have not been born yet")

        # end of validations
        if len(errors) == 0:
            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'],
                                           email=data['email'], password=data['password'])

            return {
                'new': new_user,
                'error_list': None
            }

        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }

    def login(self, log_data):
        errors = []

        try:
            found_user = User.objects.get(email=log_data['email'])
            #            print(found_user.values())
            if bcrypt.hashpw(log_data['password'].encode('utf-8'),
                             found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect password.")

        except:
            errors.append("Email address is not registered")
        if len(errors) == 0:
            return {
                'log_user': found_user,
                'list_errors': None
            }
        else:
            return {
                'log_user': None,
                'list_errors': errors
            }
class AppointmentManager(models.Manager):
    def appoint(self, data):
        errors = []
        # appointment validation
        if data['date'] == '':
            errors.append("Must enter a Date.")

        if data['time'] == '':
            errors.append("Please Enter a Time")
        if data['task'] == '':
            errors.append("Can not leave task field blank.")

        if len(errors) == 0:
            user = User.objects.get(id=data['user'])
            new_appointment = Appointment.objects.create(task=data['task'], time=data['time'], date=data['date'], user=user)
            return {
                'created_appointment': new_appointment,
                'list_errors': None
            }
        else:
            return {
                'log_user': None,
                'list_errors': errors
            }


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(null=True, max_length=250)
    password = models.CharField(max_length=250)
    dob = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=300)
    status = models.CharField(max_length=40, default="pending")
    user = models.ForeignKey(User, related_name="user")
    time = models.TimeField(auto_now=False, auto_now_add=False)
    date = models.DateField(auto_now=False, null=True)
    timestamp = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()


























