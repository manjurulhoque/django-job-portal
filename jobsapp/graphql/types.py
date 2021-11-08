from graphene_django import DjangoObjectType

from jobsapp.models import Job


class JobGQLType(DjangoObjectType):
    class Meta:
        model = Job
        fields = "__all__"
