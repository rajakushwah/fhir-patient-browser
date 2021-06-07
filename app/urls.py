from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.home,name='home' ),
    path('observation/',views.observation,name='observation' ),
    path('encounter/',views.encounter,name='encounter' ),
    path('jsonviewPatient/<id>/',views.jsonviewPatient, name='jsonviewPatient' ),
    path('jsonviewObservation/<id>/', views.jsonviewObservation, name='jsonviewObservation'),
    path('jsonviewEncounter/<id>/', views.jsonviewEncounter, name='jsonviewEncounter'),
    path('url/', views.url, name='url'),

]