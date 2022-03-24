from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('books', views.books),
    path('books/add_book', views.add_book),
    path('books/<int:book_id>', views.about_book),
    path('books/<int:book_id>/like', views.like),
    path('books/<int:book_id>/unlike', views.unlike),
    path('books/<int:book_id>/edit', views.edit),
    path('books/<int:book_id>/delete', views.delete)
]