from django import forms
from django.utils.translation import ugettext as _

from jobsapp.models import Applicant, Job


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = (
            "user",
            "created_at",
        )
        labels = {
            "last_date": _("Last Date"),
            "company_name": _("Company Name"),
            "company_description": _("Company Description"),
        }

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job


class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ("job",)
