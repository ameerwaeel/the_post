# main_app/serializers.py
from rest_framework import serializers
from .models import *
# from .serializers import ProjectsSerializer  # تأكد إنها مستوردة

class OurWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurWorks
        fields = ['name', 'description', 'rightcolor', 'leftcolor', 'link', 'main_img', 'left_img','right_img','updated_at' ,'created_at']

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = ['email','updated_at' ,'created_at' ]

class WhoWeAreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoWeAre
        fields = ['name', 'position', 'whoimg','updated_at' ,'created_at' ]

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logo
        fields = ['name', 'link', 'logoimg','updated_at' ,'created_at' ]


class OurSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurSolution
        fields = ['text', 'answer','updated_at' ,'created_at' ]

class OurResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurResults
        fields = ['before_img', 'after_img', 'after_description', 'before_descrition', 'updated_at' ,'created_at' ]

class ImgsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imgs
        fields = ['img', 'title', 'description', 'updated_at' ,'created_at' ]

# class ProjectsSerializer(serializers.ModelSerializer):
#     our_solution = OurSolutionSerializer(many=True, read_only=True)
#     imges = ImgsSerializer(many=True , read_only=True)
#     our_results = OurResultsSerializer(many=True , read_only=True)    
#     class Meta:
#         model = Projects
#         fields = ['name', 'description', 'link', 'main_img', 'logo', 'problem_defination', 'our_solution', 'imges', 'our_results','updated_at' ,'created_at' ]

class ProjectsSerializer(serializers.ModelSerializer):
    our_solution = OurSolutionSerializer(many=True, read_only=True)
    imges = ImgsSerializer(many=True, read_only=True)
    our_results = OurResultsSerializer(many=True, read_only=True)

    class Meta:
        model = Projects
        fields = [
            'name', 'description', 'link', 'main_img', 'logo',
            'problem_defination', 'our_solution', 'imges', 'our_results',
            'updated_at', 'created_at'
        ]


class ProjectsCreateSerializer(serializers.ModelSerializer):
    our_solution = serializers.ListField(child=serializers.CharField())
    imges = serializers.ListField(child=serializers.CharField())
    our_results = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Projects
        fields = [
            'name', 'description', 'link', 'main_img', 'logo',
            'problem_defination', 'our_solution', 'imges', 'our_results'
        ]

    def create(self, validated_data):
        our_solution_data = validated_data.pop("our_solution", [])
        imges_data = validated_data.pop("imges", [])
        our_results_data = validated_data.pop("our_results", [])

        project = Projects.objects.create(**validated_data)

        for text in our_solution_data:
            obj = OurSolution.objects.filter(text=text).first()
            if obj:
                project.our_solution.add(obj)

        for title in imges_data:
            obj = Imgs.objects.filter(title=title).first()
            if obj:
                project.imges.add(obj)

        for desc in our_results_data:
            obj = OurResults.objects.filter(after_description=desc).first()
            if obj:
                project.our_results.add(obj)

        # 👇 رجّع الـ serialized data باستخدام ProjectsSerializer
        return project
