from django.contrib import admin

from resume_cv.models import ResumeCv, ResumeCvCategory, ResumeCvTemplate

admin.site.register(ResumeCv)
admin.site.register(ResumeCvCategory)
admin.site.register(ResumeCvTemplate)
