from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        password1 = postData['password']
        password2 = postData['confirm']
        if len(postData['username']) < 3:
            errors["username"] = "Username should not be less than 2 characters"
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
            errors["duplicate_email"] = "Email address already being used"
        username_check = User.objects.filter(username=postData['username'])
        if len(username_check) >= 1:
            errors["duplicate_username"] = "Username already exists"
        return errors

class PostManager(models.Manager):
    def post_validator(self, postData):
        errors = {}
        if len(postData['post_content']) < 5:
            errors['post_content'] = "Post must be more than 5 characters"
        return errors

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        if len(postData['comm_content']) < 3:
            errors['comm_content'] = "Comment must be more than 3 characters"
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Plant(models.Model):
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    plant_image =models.ImageField(upload_to='plant_image', blank=True)
    watering = models.CharField(max_length=255)
    lighting = models.CharField(max_length=255)
    temp = models.CharField(max_length=255)
    soil = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owned_by = models.ForeignKey(User, related_name="plants_owned", null=True, on_delete = models.CASCADE)
    wanted_by = models.ForeignKey(User, related_name="plants_wanted", null=True, on_delete = models.CASCADE)

class Post(models.Model):
    post_content = models.TextField()
    post_image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name="posts_added", on_delete = models.CASCADE)
    objects = PostManager()

class Comment(models.Model):
    comm_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comm_by = models.ForeignKey(User, related_name="comms_added", on_delete = models.CASCADE)
    comm_post = models.ForeignKey(Post, related_name="posts_comments", on_delete = models.CASCADE)
    liked_by = models.ForeignKey(User, related_name="comms_liked", null=True, on_delete = models.CASCADE)
    objects = CommentManager()
