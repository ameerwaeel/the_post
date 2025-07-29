# main_app/serializers.py
from rest_framework import serializers
from .models import *
# from .serializers import ProjectsSerializer  # تأكد إنها مستوردة

class OurWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurWorks
        fields = ['name', 'description','rightcolorfrom','rightcolorto','leftcolorfrom', 'leftcolorto',  'link', 'main_img', 'left_img','right_img','updated_at' ,'created_at']

class WhoWeAreSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoWeAre
        fields = ['name', 'position', 'whoimg','updated_at' ,'created_at' ]

class DescriptionTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionTags
        fields = ['name' ]


class DirectionSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectionSection
        fields = ['direction' ]

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
    direction = DirectionSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Imgs
        fields = ['img', 'title', 'description', 'updated_at' ,'created_at','direction' ]

class BrandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branding
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
    imges = serializers.SerializerMethodField()
    our_results = OurResultsSerializer(many=True, read_only=True)
    branding=BrandingSerializer(many=True, read_only=True)
    description_tags=DescriptionTagsSerializer(many=True, read_only=True)
    class Meta:
        model = Projects
        fields = [
            'name', 'description', 'link', 'main_img', 'logo',
            'problem_defination', 'our_solution', 'imges', 'our_results','logo_card',
            'updated_at', 'created_at','branding','description_tags','description_card'
        ]
    def get_imges(self, obj):
        result = {}
        directions = ['left', 'center', 'right']
        for dir in directions:
            img_obj = obj.imges.filter(direction__direction__icontains=dir).first()
            if img_obj:
                data = ImgsSerializer(img_obj).data
                result[dir] = data
        return result
    
    # def get_imges(self, obj):
    #     result = {}
    #     directions = ['left', 'center', 'right']

    #     for dir in directions:
    #         img_obj = obj.imges.filter(direction__direction__icontains=dir).first()
    #         if img_obj:
    #             data = ImgsSerializer(img_obj).data
    #             if data['img'].startswith("http://127.0.0.1:8000"):
    #                 data['img'] = data['img'].replace("http://127.0.0.1:8000", "")
    #             result[dir] = data

    #     return result

    # def get_imges(self, obj):
    #     result = {}
    #     directions = ['left', 'center', 'right']

    #     for dir in directions:
    #         img_obj = obj.imges.filter(direction__direction__icontains=dir).first()
    #         if img_obj:
    #             # استخدم serializer لتحويله
    #             data = ImgsSerializer(img_obj).data
    #             # لو عايز تشيل اسم الدومين من الرابط
    #             if data['img'].startswith("http://127.0.0.1:8000"):
    #                 data['img'] = data['img'].replace("http://127.0.0.1:8000", "")
    #             result[dir] = data

    #     return result
    
class ProjectsCreateSerializer(serializers.ModelSerializer):
    our_solution = serializers.ListField(child=serializers.CharField())
    imges = serializers.ListField(child=serializers.CharField())
    our_results = serializers.ListField(child=serializers.CharField())
    description_tags = serializers.ListField(child=serializers.CharField(), required=False)
    branding = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Projects
        fields = [
            'name', 'description', 'link', 'main_img', 'logo','logo_card',
            'problem_defination', 'our_solution', 'imges', 'our_results'
            , 'description_tags', 'description_card','branding'
        ]
    def create(self, validated_data):
        # pop القيم المرتبطة بالعلاقات
        our_solution_data = validated_data.pop("our_solution", [])
        imges_data = validated_data.pop("imges", [])
        our_results_data = validated_data.pop("our_results", [])
        branding_data = validated_data.pop("branding", [])
        description_tags_data = validated_data.pop("description_tags", [])

        # إنشاء المشروع الأساسي
        project = Projects.objects.create(**validated_data)

        # ربط العلاقات
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

        for brand in branding_data:
            # obj = Branding.objects.filter(title=brand).first()
            obj = Branding.objects.filter(title=brand).first()
    
            if obj:
                project.branding.add(obj)

        for tag in description_tags_data:
            obj = DescriptionTags.objects.filter(tag=tag).first()
            if obj:
                project.description_tags.add(obj)

        return project
    
    # def create(self, validated_data):
    #     our_solution_data = validated_data.pop("our_solution", [])
    #     imges_data = validated_data.pop("imges", [])
    #     our_results_data = validated_data.pop("our_results", [])

    #     project = Projects.objects.create(**validated_data)

    #     for text in our_solution_data:
    #         obj = OurSolution.objects.filter(text=text).first()
    #         if obj:
    #             project.our_solution.add(obj)

    #     for title in imges_data:
    #         obj = Imgs.objects.filter(title=title).first()
    #         if obj:
    #             project.imges.add(obj)

    #     for desc in our_results_data:
    #         obj = OurResults.objects.filter(after_description=desc).first()
    #         if obj:
    #             project.our_results.add(obj)

    #     # 👇 رجّع الـ serialized data باستخدام ProjectsSerializer
    #     return project



class HomepageProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepageProjects
        fields = ['name', 'description', 'subdescription', 'main_img', 'link','logo','updated_at' ,'created_at']
class CountersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counters
        fields = ['startup_numbers', 'startup_description', 'strategies_numbers', 'strategies_description', 'subscribbers_numbers',  'subscribbers_description','updated_at' ,'created_at']
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['name','updated_at' ,'created_at']




