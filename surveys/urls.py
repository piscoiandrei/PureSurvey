from django.urls import path
from . import views

app_name = 'surveys'
urlpatterns = [
    path('', views.home, name='home'),
    path('survey/<str:pk>', views.survey, name="survey"),
    path('result/<str:pk>', views.results, name="results")
]
