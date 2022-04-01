from django import forms

from resume_cv.models import ResumeCv


class ResumeCvForm(forms.ModelForm):
    class Meta:
        model = ResumeCv
        exclude = ("user", "view_count", "is_published")
