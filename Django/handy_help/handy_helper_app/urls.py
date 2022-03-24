from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login), 
    path('logout', views.logout),  
    path('dashboard', views.dashboard),
    path('jobs/new', views.new),
    path('jobs/create', views.create),
    path('jobs/<int:id_number>', views.about),
    path('jobs/<int:id_number>/edit', views.edit),
    path('jobs/<int:id_number>/update', views.update),
    path('jobs/<int:id_number>/destroy', views.destroy),
    path('jobs/<int:id_number>/add', views.add),
    path('jobs/<int:id_number>/release', views.release),
]