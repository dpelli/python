from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Plant, Post, Comment
import bcrypt

def index(request):
    return render(request, "index.html")

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
                username=request.POST['username'],
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

def dashboard(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_plants': Plant.objects.all()
        }
        return render(request, 'dashboard.html', context)
    return redirect("/")

def browse(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_plants': Plant.objects.all()
        }
        return render(request, 'browse.html', context)
    return redirect("/")

def community(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_posts': Post.objects.all(),
            'all_comms': Comment.objects.all()
        }
        return render(request, 'community.html', context)
    return redirect("/")

def about(request, id_number):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'plant': Plant.objects.get(id=id_number)
        }
        return render(request, 'about.html', context)
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def add_own(request, id_number):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        plant = Plant.objects.get(id=id_number)

        plant.owned_by = user
        plant.save()
        return redirect("/browse")
    return redirect("/")

def add_own_dash(request, id_number):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        plant = Plant.objects.get(id=id_number)

        plant.owned_by = user
        plant.save()
        return redirect("/dashboard")
    return redirect("/")

def add_wish(request, id_number):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        plant = Plant.objects.get(id=id_number)

        plant.wanted_by = user
        plant.save()
        return redirect("/browse")
    return redirect("/")

def remove(request, id_number):
    if 'user_id' in request.session:
        plant = Plant.objects.get(id=id_number)
        plant.owned_by = None
        plant.save()
        return redirect("/dashboard")
    return redirect("/")

def remove_wish(request, id_number):
    if 'user_id' in request.session:
        plant = Plant.objects.get(id=id_number)
        plant.wanted_by = None
        plant.save()
        return redirect("/dashboard")
    return redirect("/")

def post(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            errors = Post.objects.post_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/community')
            else:
                request.session['post_content'] = request.POST['post_content']
                request.session['post_image'] = request.POST['post_image']

                user = User.objects.get(id=request.session['user_id'])
                post = Post.objects.create(post_content=request.session['post_content'],
                    post_image=request.session['post_image'], 
                    posted_by=user)
                user.posts_added.add(post)
                return redirect('/community')
    return redirect("/")

def like_comm(request, id_number):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        comm = Comment.objects.get(id=id_number)
        comm.liked_by = user
        comm.save()
        return redirect("/community")
    return redirect("/")

def comment(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            request.session['comm_content'] = request.POST['comm_content']
            request.session['post_id'] = request.POST['post_id']

            user = User.objects.get(id=request.session['user_id'])
            post = Post.objects.get(id=request.session['post_id'])
            comm = Comment.objects.create(comm_content=request.session['comm_content'],
                comm_post=post,
                comm_by=user)
            user.comms_added.add(comm)
            post.posts_comments.add(comm)
            return redirect('/community')
    return redirect("/")