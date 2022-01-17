import graphene

from jobsapp.graphql.graphql_mixins import DynamicArgsMixin, MutationMixin, CreateNewJobMixin
from jobsapp.graphql.permissions import IsAuthenticated, IsEmployer


class CreateNewJob(MutationMixin, DynamicArgsMixin, CreateNewJobMixin, graphene.Mutation):
    __doc__ = CreateNewJobMixin.__doc__

    __required_args = {
        'title': 'String',
        'description': 'String',
        'location': 'String',
        'type': 'String',
        'category': 'String',
        'last_date': 'String',
        'company_name': 'String',
        'company_description': 'String',
        'website': 'String',
        'created_at': 'String',
        'salary': 'Int',
    }
    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]
