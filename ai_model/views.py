from django.shortcuts import render

# Create your views here.
# leads/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InputLead, LeadOutput
from .serializers import InputLeadSerializer, LeadOutputSerializer
import requests
import json

# class LeadProcessView(APIView):
#     def post(self, request):
#         input_serializer = InputLeadSerializer(data=request.data)
#         if input_serializer.is_valid():
#             input_lead = input_serializer.save()

#             # إرسال إلى n8n webhook
#             n8n_url = "https://YOUR_N8N_WEBHOOK_URL"
#             n8n_response = requests.post(n8n_url, json=[input_serializer.data])

#             if n8n_response.status_code == 200:
#                 output_raw = n8n_response.json().get("output", "")
#                 if output_raw:
#                     try:
#                         output_json = json.loads(output_raw.replace("json", "").strip())

#                         lead_output = LeadOutput.objects.create(
#                             input_lead=input_lead,
#                             qualification_status=output_json.get("qualification_status"),
#                             reason=output_json.get("reason"),
#                             proposed_title=output_json["proposed_solution"].get("title"),
#                             proposed_description=output_json["proposed_solution"].get("description"),
#                             estimated_cost=output_json["proposed_solution"].get("estimated_cost"),
#                             implementation_time=output_json["proposed_solution"].get("implementation_time"),
#                             next_step=output_json.get("next_step"),
#                             generated_email=output_json.get("generated_email"),
#                         )

#                         return Response({
#                             "input": InputLeadSerializer(input_lead).data,
#                             "output": LeadOutputSerializer(lead_output).data
#                         }, status=status.HTTP_201_CREATED)

#                     except Exception as e:
#                         return Response({"error": f"Failed to parse output: {str(e)}"}, status=500)

#             return Response({"error": "n8n processing failed"}, status=500)

#         return Response(input_serializer.errors, status=400)
# leads/views.py

class LeadProcessView(APIView):
    def post(self, request):
        input_serializer = InputLeadSerializer(data=request.data)
        if input_serializer.is_valid():
            input_lead = input_serializer.save()

            # إرسال البيانات إلى n8n
            n8n_url = "https://YOUR_REAL_N8N_WEBHOOK_URL"
            try:
                n8n_response = requests.post(n8n_url, json=[input_serializer.data])
            except requests.exceptions.RequestException as e:
                return Response({"error": f"Connection failed: {str(e)}"}, status=500)

            if n8n_response.status_code == 200:
                output_raw = n8n_response.json().get("output", "")
                if output_raw:
                    try:
                        output_json = json.loads(output_raw.replace("json", "").strip())

                        lead_output = LeadOutput.objects.create(
                            input_lead=input_lead,
                            project_summary=output_json.get("Project Evaluation Summary", ""),
                            budget_summary=output_json.get("Budget Evaluation Summary", ""),
                            timeline_summary=output_json.get("Timeline Evaluation Summary", ""),
                            recommended_budget=output_json.get("Recommended Budget", ""),
                            recommended_duration=output_json.get("Recommended Duration", ""),
                            task_breakdown=output_json.get("Task Breakdown by Phase", {}),
                        )

                        return Response({
                            "input": InputLeadSerializer(input_lead).data,
                            "output": LeadOutputSerializer(lead_output).data
                        }, status=status.HTTP_201_CREATED)

                    except Exception as e:
                        return Response({"error": f"Failed to parse output: {str(e)}"}, status=500)

            return Response({"error": "n8n processing failed"}, status=500)

        return Response(input_serializer.errors, status=400)
