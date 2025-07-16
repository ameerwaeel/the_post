# main_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('ourworks/', OurWorksListCreateView.as_view()),
    path('ourworks/<uuid:uuid>/', OurWorksDetailView.as_view()),

    path('newsletter/', NewsLetterListCreateView.as_view()),
    path('newsletter/<uuid:uuid>/', NewsLetterDetailView.as_view()),

    path('whoweare/', WhoWeAreListCreateView.as_view()),
    path('whoweare/<uuid:uuid>/', WhoWeAreDetailView.as_view()),

    path('logos/', LogoListCreateView.as_view()),
    path('logos/<uuid:uuid>/', LogoDetailView.as_view()),

    path('projects/', ProjectsListCreateView.as_view()),
    path('projects/<uuid:uuid>/', ProjectsDetailView.as_view()),

    path('oursolution/', OurSolutionListCreateView.as_view()),
    path('oursolution/<uuid:uuid>/', OurSolutionDetailView.as_view()),

    path('ourresults/', OurResultsListCreateView.as_view()),
    path('ourresults/<uuid:uuid>/', OurResultsDetailView.as_view()),

    path('imgs/', ImgsListCreateView.as_view()),
    path('imgs/<uuid:uuid>/', ImgsDetailView.as_view()),
]
