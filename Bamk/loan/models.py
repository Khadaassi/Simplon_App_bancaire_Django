# loan/models.py
from django.db import models
from user.models import User

class LoanStatus(models.TextChoices):
    PENDING = 'pending', 'En attente'
    AI_APPROVED = 'ai_approved', 'Approuvé par IA'
    AI_REJECTED = 'ai_rejected', 'Rejeté par IA'
    ADVISOR_APPROVED = 'advisor_approved', 'Approuvé par conseiller'
    ADVISOR_REJECTED = 'advisor_rejected', 'Rejeté par conseiller'

class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=2)
    naics = models.IntegerField()
    new_exist = models.IntegerField()
    retained_job = models.IntegerField()
    franchise_code = models.IntegerField()
    urban_rural = models.IntegerField()
    gr_appv = models.FloatField()
    bank = models.CharField(max_length=255)
    term = models.IntegerField()
    prediction = models.FloatField(null=True, blank=True)  # Stockera la prédiction
    status = models.CharField(
        max_length=20,
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING
    )
    advisor_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"LoanRequest {self.id} - {self.state}"