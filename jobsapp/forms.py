from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from jobsapp.models import Applicant, Job, Company


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ("user", "created_at", "company_name", "company_description", "website")
        labels = {
            "last_date": "Last Date",
            "company": "Company profile",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].required = True
        self.fields["company"].empty_label = "Select a company"
        self.fields["company"].widget.attrs["class"] = "form-control"

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
        if job.company:
            job.company_name = job.company.name[:100]
            job.company_description = (job.company.description or "")[:300]
            job.website = (job.company.website or "")[:100]
        if commit:
            job.save()
            for tag in self.cleaned_data["tags"]:
                job.tags.add(tag)
        return job


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ("job",)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            "name",
            "description",
            "website",
            "logo",
            "industry",
            "size",
            "culture_benefits",
        )
        labels = {
            "name": "Company Name",
            "description": "Company Description",
            "website": "Company Website",
            "logo": "Company Logo",
            "industry": "Industry",
            "size": "Company Size",
            "culture_benefits": "Culture & Benefits",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "culture_benefits": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")
        if logo:
            # Validate file size (max 5MB)
            if logo.size > 5 * 1024 * 1024:
                raise ValidationError("Logo file size should not exceed 5MB.")
            # Validate file type
            if not logo.content_type.startswith("image/"):
                raise ValidationError("Please upload a valid image file.")
        return logo
