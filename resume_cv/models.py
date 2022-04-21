from time import strftime

from django.db import models
import uuid

from accounts.models import User
from utils.filename import generate_file_name


def resume_cv_directory_path(instance, filename):
    return 'resumes/{0}/{1}'.format(strftime('%Y/%m/%d'), generate_file_name() + '.' + filename.split('.')[-1])


class ResumeCvCategory(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=resume_cv_directory_path, blank=True, null=True)
    color = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResumeCvTemplate(models.Model):
    category = models.ForeignKey(ResumeCvCategory, on_delete=models.CASCADE, related_name="templates")
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=resume_cv_directory_path, blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ResumeCv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume_cvs")
    template = models.ForeignKey(ResumeCvTemplate, on_delete=models.CASCADE, related_name="resume_cvs")
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
