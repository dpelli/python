from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book
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
                email=request.POST['email'],
                password=pw_hash) 
            request.session['user_id'] = user.id
            return redirect("/books")
    return redirect("/")



def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
        messages.error(request,"Email and/or password is incorrect")
    return redirect("/")



def logout(request):
    request.session.flush()
    return redirect("/")


def books(request):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_books': Book.objects.all()
        }
        return render(request, "books.html", context)
    return redirect("/")



def add_book(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            errors = Book.objects.book_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/books')
            else:
                request.session['title'] = request.POST['title']
                request.session['desc'] = request.POST['desc']
                
            user = User.objects.get(id=request.session['user_id'])
            book = Book.objects.create(title=request.session['title'],
                desc=request.session['desc'], 
                added_by=user)
            user.books_liked.add(book)
        return redirect("/books")
    return redirect("/")




def like(request, book_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        user.books_liked.add(Book.objects.get(id=book_id))
        return redirect(f"/books/{book_id}")
    return redirect("/")



def about_book(request, book_id):
    if 'user_id' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'book': Book.objects.get(id=book_id)
        }
        return render(request, "about_book.html", context)
    return redirect("/")



def unlike(request, book_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=book_id)
        user.books_liked.remove(book)
        return redirect(f"/books/{book_id}")
    return redirect("/")


def edit(request, book_id):
    if 'user_id' in request.session:
        book = Book.objects.get(id=book_id)
        book.title = request.POST['book_title']
        book.desc = request.POST['desc']
        book.save()
        return redirect(f"/books/{book_id}")
    return redirect("/")


def delete(request, book_id):
    if 'user_id' in request.session:
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect("/books")
    return redirect("/")
