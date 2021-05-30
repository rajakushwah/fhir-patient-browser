from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.home,name='home' ),
    path('observation/',views.observation,name='observation' ),
    path('encounter/',views.encounter,name='encounter' ),
    path('jsonviewPatient/<id>/',views.jsonviewPatient, name='jsonviewPatient' ),
    path('jsonviewObservation/', views.jsonviewObservation, name='jsonviewObservation'),
    path('jsonviewEncounter/', views.jsonviewEncounter, name='jsonviewEncounter'),

    ]