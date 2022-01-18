import graphene

from jobsapp.graphql.graphql_mixins import DynamicArgsMixin, MutationMixin, CreateNewJobMixin
from jobsapp.graphql.input_types import TagInput
from jobsapp.graphql.permissions import IsAuthenticated, IsEmployer
from graphene.types import Int


class CreateNewJob(
    MutationMixin,
    DynamicArgsMixin,
    CreateNewJobMixin,
    graphene.Mutation
):
    __doc__ = CreateNewJobMixin.__doc__
    _required_args = {
        'title': 'String',
        'description': 'String',
        'location': 'String',
        'type': 'String',
        'category': 'String',
        'last_date': 'String',
        'company_name': 'String',
        'company_description': 'String',
        'website': 'String',
        'salary': 'Int',
    }
    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    class Arguments:
        tags = graphene.List(Int, required=True)
