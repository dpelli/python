from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('word_jumble', views.word_jumble),
    path('guess', views.guess),
    path('reset_jumble', views.reset_jumble),
    path('reset_hang', views.reset_hang),
    path('start_jumble', views.start_jumble),
    path('new_word', views.new_word),
    path('logout', views.logout),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('hangman', views.hangman),
    path('scoreboard', views.scoreboard),
]