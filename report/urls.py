from django.contrib import admin
from django.urls import path
from . import views
from .views import *

app_name='report'
urlpatterns = [
    path('', views.index, name="index"),
    path('LogIn/', views.signIn, name="signIn"),
    path('LogOut/', views.signOut, name="signOut"),
    path('add/', views.add_dossier, name="add"),
    path('fiche_dossier/<int:pk>', views.fiche_dossier, name="fiche_dossier"),
    path('delete/<int:pk>', views.delete, name="delete"),
    path('delete_note/<int:pk>/<int:id>', views.delete_note, name="delete_note"),

    path('waiting/<int:pk>', views.waiting, name="waiting"),
    path('closed_win/<int:pk>', views.CLOSED_WIN, name="closed_win"),
    path('closed_lost/<int:pk>', views.CLOSED_LOST, name="closed_lost"),
    path('sample/<int:pk>', views.WAITING_FOR_SAMPLE, name="sample"),

    path('Nouvelle_Note/<int:pk>', views.Nouvelle_Note, name="Nouvelle_Note"),
    path('Add_todo', views.add_Todo, name="Todo"),
    path('done/<int:pk>', views.done, name="delete_todo"),
    path('Report/', Report.as_view(), name='Report'),
    path('export_excel/', views.export_data, name='export_data'),

]
