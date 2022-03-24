from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name should be at least 3 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # if not EMAIL_REGEX.match(postData['email_address']):            
        #     errors['email_address'] = ("Invalid email address!")
        if len(postData['email_address']) == 0:
            errors['email_address'] = "You must enter an email"
        elif not EMAIL_REGEX.match(postData['email_address']):
            errors['email_address'] = "Must be a valid email"

        current_users = User.objects.filter(email_address = postData['email_address'])
        if len(current_users) > 0:
            errors['duplicate'] = "that email is already in use."

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"

        return errors

    def login_validator(self, postData):
        errors = {}
        existing_user = User.objects.filter(email_address=postData['email_address'])
        print(existing_user)
        if len(postData['email_address']) == 0:
            errors['email_address'] = "Email must be entered"
        if len(postData['password']) < 8:
            errors['password'] = "An 8 character password must be entered"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['password'] = "email and password do not match"
        return errors


class User(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return '{} {}' .format(self.first_name, self.last_name)

class Word(models.Model):
    name = models.CharField(max_length=64)
    length = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
