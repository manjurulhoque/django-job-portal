from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from jobsapp.models import Applicant, Job


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ("user", "created_at")
        labels = {
            "last_date": "Last Date",
            "company_name": "Company Name",
            "company_description": "Company Description",
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def clean_last_date(self):
        date = self.cleaned_data["last_date"]
        if date.date() < datetime.now().date():
            raise ValidationError("Last date can't be before from today")
        return date

    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        if len(tags) > 6:
            raise forms.ValidationError("You can't add more than 6 tags")
        return tags

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
            for tag in self.cleaned_data["tags"]:
                job.tags.add(tag)
        return job


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ("job",)
