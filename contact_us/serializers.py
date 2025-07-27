from rest_framework import serializers
from .models import *

class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = ['email','updated_at' ,'created_at' ]

class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = ['name','updated_at' ,'created_at' ]


class ContactUSSerializer(serializers.ModelSerializer):
    # interests = serializers.PrimaryKeyRelatedField(queryset=Interests.objects.all())
    interests = serializers.SlugRelatedField(
        queryset=Interests.objects.all(),
        slug_field='name'  # أو أي حقل ثاني زي slug
    )    
    class Meta:
        model = ContactUS
        fields = ['full_name', 'email', 'phone', 'company_name', 'comment', 'budget', 'file', 'interests', 'updated_at' ,'created_at' ]


class ChatContactUSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatContactUS
        fields = ['full_name', 'email', 'phone', 'company_name', 'comment', 'session', 'link', 'updated_at' ,'created_at' ]                        