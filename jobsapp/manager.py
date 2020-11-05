from django.db import models


class JobManager(models.Manager):
    def filled(self, *args, **kwargs):
        return self.filter(filled=True, *args, **kwargs)

    def unfilled(self, *args, **kwargs):
        return self.filter(filled=False, *args, **kwargs)
