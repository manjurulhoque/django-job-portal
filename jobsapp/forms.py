from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from jobsapp.models import Applicant, Job, Company


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ("user", "created_at", "updated_at", "slug", "website")
        labels = {
            "application_deadline": "Application deadline",
            "workplace_type": "Workplace type",
            "experience_level": "Experience level",
            "salary_currency": "Salary currency",
            "salary_period": "Salary period",
            "company": "Company profile",
        }
        widgets = {
            "workplace_type": forms.Select(attrs={"class": "form-control"}),
            "experience_level": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "salary_period": forms.Select(attrs={"class": "form-control"}),
            "application_deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].required = True
        self.fields["company"].empty_label = "Select a company"
        self.fields["company"].widget.attrs["class"] = "form-control"
        self.fields["salary_currency"].widget = forms.Select(
            choices=[
                ("BDT", "BDT"),
                ("USD", "USD"),
                ("EUR", "EUR"),
                ("GBP", "GBP"),
                ("INR", "INR"),
            ],
            attrs={"class": "form-control"},
        )
        for name in (
            "title",
            "location",
            "type",
            "salary",
            "vacancy",
            "salary_min",
            "salary_max",
        ):
            if name in self.fields:
                self.fields[name].widget.attrs["class"] = "form-control"

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def clean_application_deadline(self):
        date = self.cleaned_data["application_deadline"]
        if date.date() < datetime.now().date():
            raise ValidationError("Application deadline can't be before today")
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
