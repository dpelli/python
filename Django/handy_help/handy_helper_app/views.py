from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job
import bcrypt
from datetime import datetime, date
import time

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
            user = User.objects.create(first_name=request.POST['first_name'], 
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash) 
            request.session['user_id'] = user.id
            return redirect("/dashboard")
    return redirect("/")

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/dashboard')
        messages.error(request,"Email and/or password is incorrect")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def dashboard(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_jobs': Job.objects.all()
        }
        return render(request, 'dashboard.html', context)
    return redirect("/")

def new(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'new.html', context)
    return redirect("/")

def create(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            errors = Job.objects.job_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/jobs/new')
            else:
                request.session['title'] = request.POST['title']
                request.session['desc'] = request.POST['desc']
                request.session['location'] = request.POST['location']

                user = User.objects.get(id=request.session['user_id'])
                job = Job.objects.create(title=request.session['title'],
                    desc=request.session['desc'], 
                    location=request.session['location'], 
                    added_by=user)
                user.jobs_added.add(job)
                return redirect('/dashboard')
    return redirect("/")

def about(request, id_number):
    job = Job.objects.get(id=id_number)
    date_posted = datetime.strftime(job.created_at, "%Y-%m-%d")
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'job': Job.objects.get(id=id_number),
        'date_posted': date_posted
    }
    return render(request, 'about.html', context)

def edit(request, id_number):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'job': Job.objects.get(id=id_number)
        }
        return render(request, 'edit.html', context)
    return redirect("/")

def update(request, id_number):
    if 'user_id' in request.session:
        if request.method == "POST":
            job = Job.objects.get(id=id_number)
            errors = Job.objects.job_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/jobs/{job.id}/edit')
            else:
                job.title = request.POST['title']
                job.desc = request.POST['desc']
                job.location = request.POST['location']
                job.save()
                return redirect("/dashboard")
    return redirect("/")

def destroy(request, id_number):
    if 'user_id' in request.session:
        job_to_delete = Job.objects.get(id=id_number)
        job_to_delete.delete()
        return redirect("/dashboard")
    return redirect("/")

def add(request, id_number):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        job = Job.objects.get(id=id_number)

        job.taken_by = user
        job.save()
        return redirect("/dashboard")
    return redirect("/")

def release(request, id_number):
    if 'user_id' in request.session:
        job = Job.objects.get(id=id_number)
        job.taken_by = None
        job.save()
        return redirect("/dashboard")
    return redirect("/")