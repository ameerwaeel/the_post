# main_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('ourworks/', OurWorksListCreateView.as_view()),
    path('ourworks/<uuid:uuid>/', OurWorksDetailView.as_view()),

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

    path('HomepageProjects/', HomepageProjectsListCreateView.as_view()),
    path('HomepageProjects/<uuid:uuid>/', HomepageProjectsDetailView.as_view()),

    path('Counters/', CountersListCreateView.as_view()),
    path('Counters/<uuid:uuid>/', CountersDetailView.as_view()),
    
    path('Services/', ServicesListCreateView.as_view()),
    path('Services/<uuid:uuid>/', ServicesDetailView.as_view()),
    
    path('DescriptionTag/', DescriptionTagsListCreateView.as_view()),
    path('DescriptionTag/<uuid:uuid>/', DescriptionTagsDetailView.as_view()),

    path('DirectionSection/', DirectionSectionListCreateView.as_view()),
    path('DirectionSection/<uuid:uuid>/', DirectionSectionDetailView.as_view()),

    path('Branding/', BrandingListCreateView.as_view()),
    path('Branding/<uuid:uuid>/', BrandingDetailView.as_view()),            
]
