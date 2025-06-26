from django.db import models

# Create your models here.
# leads/models.py

from django.db import models

class InputLead(models.Model):
    need = models.CharField(max_length=255)
    email = models.EmailField()
    budget = models.IntegerField()
    timeline = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.need}"


# class LeadOutput(models.Model):
#     input_lead = models.OneToOneField(InputLead, on_delete=models.CASCADE, related_name="output")

#     qualification_status = models.CharField(max_length=50)
#     reason = models.TextField()
    
#     proposed_title = models.CharField(max_length=255)
#     proposed_description = models.TextField()
#     estimated_cost = models.CharField(max_length=100)
#     implementation_time = models.CharField(max_length=100)

#     next_step = models.TextField()
#     generated_email = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Output for {self.input_lead.email}"
# leads/models.py

class LeadOutput(models.Model):
    input_lead = models.OneToOneField(InputLead, on_delete=models.CASCADE, related_name="output")

    project_summary = models.TextField()
    budget_summary = models.TextField()
    timeline_summary = models.TextField()

    recommended_budget = models.CharField(max_length=100)
    recommended_duration = models.CharField(max_length=100)

    task_breakdown = models.JSONField()  # هذا حقل جديد لتخزين dict كامل

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Output for {self.input_lead.email}"
