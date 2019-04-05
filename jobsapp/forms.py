from django import forms

from jobsapp.models import Job


class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user',)

    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        print(self._errors)
        return valid
