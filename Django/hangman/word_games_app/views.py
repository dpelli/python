from django.shortcuts import render, redirect
from django.contrib import messages
from english_words import english_words_lower_alpha_set
# added ^ to see if I can pull from a larger dictionary 
import random
import bcrypt
# from random_word import RandomWords    # this line of code is not being used 

from .models import *


# words = ["python", 
#     "jumble", 
#     "easy", 
#     "difficult", 
#     "answer", 
#     "xylophone"
# ]

# words = [ "english_words"
# ]

def index(request):
    return render(request, 'index.html')

def rword(request):
    level = request.session['level']
    # difficulty = request.session['difficulty']
    # theme = request.session['theme']

    if (level == "1"):
        all_words = Word.objects.filter(length=4)
    elif (level == "2"):
        all_words = Word.objects.filter(length=5)
    else:
        all_words = Word.objects.filter(length=6)

    word = random.choice(all_words)
    print(word.name)
    request.session['word'] = word.name
    jumble = random.sample(word.name, len(word.name)) #return a list of letters
    jumbled_word = "".join(jumble)
    request.session['jumbled_word'] = jumbled_word

    return request.session['jumbled_word']

def start_jumble(request):
    request.session['level'] = request.POST['level']
    request.session['difficulty'] = request.POST['difficulty']
    request.session['theme'] = request.POST['theme']
        # difficulty = request.session['difficulty']
    # theme = request.session['theme']
    print(request.session['level'])
    if (request.session['level'] == "1"):
        all_words = Word.objects.filter(length=4)
    elif (request.session['level'] == "2"):
        all_words = Word.objects.filter(length=5)
    elif (request.session['level'] == "20"):
        all_words = Word.objects.filter(length=10)
    else:
        all_words = Word.objects.filter(length=6)

    word = random.choice(all_words)
    print(word.name)
    request.session['word'] = word.name
    jumble = random.sample(word.name, len(word.name)) #return a list of letters
    jumbled_word = "".join(jumble)
    request.session['jumbled_word'] = jumbled_word
    
    return redirect("/word_jumble")
    
def word_jumble(request):
    if 'answer' not in request.session:
        request.session['answer'] = ""
    # rword(request)
    print(request.session['level'])
    context = {
        'jumbled_word': request.session['jumbled_word'],
        'answer': request.session['answer']
    }
    return render(request, 'word_jumble.html', context)

def guess(request):
    guess = request.POST['guess']
    if guess != request.session['word']:
        request.session['answer'] = "Wrong!"
    else:
        request.session['answer'] = "Correct!"
    return redirect("/word_jumble")

def new_word(request):
    rword(request)
    return redirect("/word_jumble")

def reset_jumble(request):
    request.session['answer'] = ""
    request.session['jumbled_word'] = ""
    request.session['level'] = ""
    print(request.session['level'])
    print("hello")
    return redirect("/dashboard")

def reset_hang(request):
    # request.session.flush()
    return redirect("/hangman")

def logout(request):
    request.session.flush()
    return redirect("/")


def register(request):

    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/')

    if request.method == "POST":
    #     User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=request.POST['password'])
    # return redirect('/')

        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=hashed_pw
        )
        request.session['user_id'] = new_user.id
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email_address = request.POST['email_address'])
        request.session['user_id'] = this_user[0].id
        return redirect('/dashboard')
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = User.objects.get(id=request.session['user_id'])
    # my_jobs = Job.objects.get(id=request.session['job_id'])
    context = {
        # "all_jobs": Job.objects.all(),
        'user_id': user_id,
        'users_id': User.objects.all(),
        # "my_jobs": Job.objects.get(id=job_id)
    }
    return render(request, 'dashboard.html', context)

def hangman(request):
    return render(request, 'hangman.html')

def scoreboard(request):
    return render(request, 'scoreboard.html')