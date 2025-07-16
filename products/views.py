from django.shortcuts import render

# Create your views here.
# main_app/views.py
from rest_framework import generics
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
# from django.http import Http404
# from rest_framework.response import Response
# from rest_framework import status   
# from rest_framework import viewsets
# from rest_framework.views import APIView  
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from rest_framework.decorators import action
# from django.shortcuts import get_object_or_404
# from django.http import Http404
# from rest_framework import generics
# from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

class OurWorksListCreateView(generics.ListCreateAPIView):
    queryset = OurWorks.objects.all()
    serializer_class = OurWorksSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class OurWorksDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OurWorks.objects.all()
    serializer_class = OurWorksSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

class NewsLetterListCreateView(generics.ListCreateAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class NewsLetterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsLetter.objects.all()
    serializer_class = NewsLetterSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

class WhoWeAreListCreateView(generics.ListCreateAPIView):
    queryset = WhoWeAre.objects.all()
    serializer_class = WhoWeAreSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]


class WhoWeAreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WhoWeAre.objects.all()
    serializer_class = WhoWeAreSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

class LogoListCreateView(generics.ListCreateAPIView):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class LogoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Logo.objects.all()
    serializer_class = LogoSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'



class ProjectsListCreateView(generics.ListCreateAPIView):
    queryset = Projects.objects.all()
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProjectsCreateSerializer
        return ProjectsSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProjectsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()

        # ✅ استخدم ProjectsSerializer للرد بالبيانات بعد الإنشاء
        response_serializer = ProjectsSerializer(project)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    
class ProjectsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

class OurSolutionListCreateView(generics.ListCreateAPIView):
    queryset = OurSolution.objects.all()
    serializer_class = OurSolutionSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class OurSolutionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OurSolution.objects.all()
    serializer_class = OurSolutionSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

class OurResultsListCreateView(generics.ListCreateAPIView):
    queryset = OurResults.objects.all()
    serializer_class = OurResultsSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class OurResultsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OurResults.objects.all()
    serializer_class = OurResultsSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'

class ImgsListCreateView(generics.ListCreateAPIView):
    queryset = Imgs.objects.all()
    serializer_class = ImgsSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

class ImgsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Imgs.objects.all()
    serializer_class = ImgsSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'uuid'
