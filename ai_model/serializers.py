# leads/serializers.py

from rest_framework import serializers
from .models import InputLead, LeadOutput

class InputLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputLead
        fields = '__all__'

# class LeadOutputSerializer(serializers.ModelSerializer):
#     input_lead = serializers.PrimaryKeyRelatedField(queryset=InputLead.objects.all())

#     class Meta:
#         model = LeadOutput
#         fields = '__all__'# leads/serializers.py

class LeadOutputSerializer(serializers.ModelSerializer):
    input_lead = serializers.PrimaryKeyRelatedField(queryset=InputLead.objects.all())

    class Meta:
        model = LeadOutput
        fields = '__all__'
