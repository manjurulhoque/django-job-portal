import graphene

from . import sub_mutations as job_mutations


class JobMutation(graphene.ObjectType):
    create_job = job_mutations.CreateNewJob.Field()
    update_job = job_mutations.UpdateJob.Field()
