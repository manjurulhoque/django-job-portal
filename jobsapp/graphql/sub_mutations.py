import graphene

from jobsapp.graphql.graphql_mixins import (
    DynamicArgsMixin,
    MutationMixin,
    CreateNewJobMixin,
    UpdateJobMixin,
    SingleObjectMixin,
)
from jobsapp.graphql.input_types import TagInput
from jobsapp.graphql.permissions import IsAuthenticated, IsEmployer
from graphene.types import Int

from jobsapp.graphql.types import JobGQLType
from jobsapp.models import Job


class CreateNewJob(MutationMixin, DynamicArgsMixin, CreateNewJobMixin, graphene.Mutation):
    __doc__ = CreateNewJobMixin.__doc__
    _required_args = {
        "title": "String",
        "description": "String",
        "location": "String",
        "type": "String",
        "category": "String",
        "last_date": "String",
        "company_name": "String",
        "company_description": "String",
        "website": "String",
        "salary": "Int",
    }
    permission_classes = [IsAuthenticated, IsEmployer]

    class Arguments:
        tags = graphene.List(Int, required=True)


class UpdateJob(MutationMixin, DynamicArgsMixin, SingleObjectMixin, UpdateJobMixin, graphene.Mutation):
    job = graphene.Field(JobGQLType)
    __doc__ = UpdateJobMixin.__doc__
    _required_args = {"pk": "ID"}
    _args = {
        "title": "String",
        "description": "String",
        "location": "String",
        "type": "String",
        "category": "String",
        "last_date": "String",
        "company_name": "String",
        "company_description": "String",
        "website": "String",
        "salary": "Int",
    }

    class Arguments:
        tags = graphene.List(Int, required=False)

    permission_classes = [IsAuthenticated, IsEmployer]
    model = Job
    check_object_level_permission: bool = False
