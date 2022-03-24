from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login), 
    path('dashboard', views.dashboard),
    path('browse', views.browse),
    path('community', views.community),
    path('about/<int:id_number>', views.about),
    path('logout', views.logout),  
    path('browse/<int:id_number>/add_own', views.add_own),
    path('browse/<int:id_number>/add_wish', views.add_wish),
    path('dashboard/<int:id_number>/add_own_dash', views.add_own_dash),
    path('dashboard/<int:id_number>/remove', views.remove),
    path('dashboard/<int:id_number>/remove_wish', views.remove_wish),
    path('post', views.post),
    path('comment', views.comment),
    path('community/<int:id_number>/like', views.like_comm),
]
