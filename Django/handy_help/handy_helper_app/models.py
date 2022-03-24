from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        password1 = postData['password']
        password2 = postData['confirm']
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should not be less than 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should not be less than 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = ("Invalid email address")
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if password1 != password2:
            errors["confirm"] = "Passwords did not match"
        user_email_check = User.objects.filter(email=postData['email'])
        if len(user_email_check) >= 1:
            errors["duplicate"] = "Email address already being used"
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "Title must be more than 3 characters"
        if len(postData['desc']) < 3:
            errors["desc"] = "Descriptionn must be more than 3 characters"
        if len(postData['location']) < 3:
            errors["location"] = "Location must be more than 3 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name="jobs_added", on_delete = models.CASCADE)
    taken_by = models.ForeignKey(User, related_name="jobs_taken", null=True, on_delete = models.CASCADE)
    objects = JobManager()