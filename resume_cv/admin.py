from django.contrib import admin

from resume_cv.models import ResumeCv
from resume_cv.models import ResumeCvCategory
from resume_cv.models import ResumeCvTemplate

admin.site.register(ResumeCv)
admin.site.register(ResumeCvCategory)
admin.site.register(ResumeCvTemplate)
