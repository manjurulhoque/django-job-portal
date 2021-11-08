import graphene

from .types import JobGQLType
from jobsapp.models import Job


class JobQuery(graphene.ObjectType):
    jobs = graphene.List(JobGQLType)

    def resolve_jobs(root, info):
        return Job.objects.all()
