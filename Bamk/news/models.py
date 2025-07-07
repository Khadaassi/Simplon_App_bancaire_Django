from django.db import models
from user.models import User
from django.core.exceptions import ValidationError


class News(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to="news_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.created_by.is_staff:
            raise ValidationError(
                "Seuls les utilisateurs staff peuvent créer des articles."
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
