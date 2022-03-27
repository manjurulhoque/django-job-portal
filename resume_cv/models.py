from django.db import models
import uuid

from accounts.models import User


class ResumeCv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume_cvs")
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
