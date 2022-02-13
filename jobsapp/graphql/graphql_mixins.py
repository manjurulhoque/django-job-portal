import graphene
import logging
from django.shortcuts import get_object_or_404
from graphene_django.types import DjangoObjectType
from typing import Optional
from django.db import transaction
from django.forms.models import model_to_dict

from accounts.graphql.constants import Messages
from .exceptions import PermissionDeniedError
from .graphql_base import Output
from ..forms import CreateJobForm

logger = logging.getLogger(__name__)


class PermissionMixin:
    permission_classes = []

    @classmethod
    def check_permissions(cls, info, **kwargs):
        request = info.context
        for permission in cls.get_permissions():
            if not permission.has_permission(request, **kwargs):
                logger.debug(
                    "Permission denied for Permission class: {}, user: {}, message: {}".format(
                        permission.__class__.__name__, str(request.user), str(getattr(permission, "message", None))
                    )
                )
                raise PermissionDeniedError(getattr(permission, "message", None))

    @classmethod
    def check_object_permissions(cls, info, obj, **kwargs):
        request = info.context
        for permission in cls.get_permissions():
            if not permission.has_object_permission(request, obj, **kwargs):
                logger.debug(
                    "Permission denied for Permission class: {}, user: {}, object: {}, message: {}".format(
                        permission.__class__.__name__,
                        str(request.user),
                        str(obj),
                        str(getattr(permission, "message", None)),
                    )
                )
                raise PermissionDeniedError(getattr(permission, "message", None))

    @classmethod
    def get_permissions(cls):
        return [permission() for permission in cls.permission_classes]


def get_permission_denied_message(cls, e: Exception):
    Messages.PERMISSION_DENIED_ERROR[0]["message"] = str(e)
    return cls(success=False, errors=Messages.PERMISSION_DENIED_ERROR)


class MutationMixin(PermissionMixin):
    """
    All mutations should extend this class
    """

    @classmethod
    def mutate(cls, root, info, **input):
        try:
            cls.check_permissions(info, **input)
            return cls.resolve_mutation(root, info, **input)
        except PermissionDeniedError as e:
            return get_permission_denied_message(cls, e)

    @classmethod
    def parent_resolve(cls, root, info, **kwargs):
        return super().mutate(root, info, **kwargs)


class RelayMutationMixin(PermissionMixin):
    """
    All relay mutations should extend this class
    """

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            cls.check_permissions(info, **kwargs)
            return cls.resolve_mutation(root, info, **kwargs)
        except PermissionDeniedError as e:
            return get_permission_denied_message(cls, e)

    @classmethod
    def parent_resolve(cls, root, info, **kwargs):
        return super().mutate_and_get_payload(root, info, **kwargs)


class DynamicArgsMixin:
    """
    A class that knows how to initialize graphene arguments

    get args from
        cls._args
        cls._required_args
    args is dict { arg_name: arg_type }
    or list [arg_name,] -> defaults to String
    """

    _args = {}
    _required_args = {}

    @classmethod
    def Field(cls, *args, **kwargs):
        if isinstance(cls._args, dict):
            for key in cls._args:
                cls._meta.arguments.update({key: graphene.Argument(getattr(graphene, cls._args[key]))})
        elif isinstance(cls._args, list):
            for key in cls._args:
                cls._meta.arguments.update({key: graphene.String()})

        if isinstance(cls._required_args, dict):
            for key in cls._required_args:
                cls._meta.arguments.update(
                    {key: graphene.Argument(getattr(graphene, cls._required_args[key]), required=True)}
                )
        elif isinstance(cls._required_args, list):
            for key in cls._required_args:
                cls._meta.arguments.update({key: graphene.String(required=True)})
        return super().Field(*args, **kwargs)


class DynamicInputMixin:
    """
    A class that knows how to initialize graphene relay input

    get inputs from
        cls._inputs
        cls._required_inputs
    inputs is dict { input_name: input_type }
    or list [input_name,] -> defaults to String
    """

    _inputs = {}
    _required_inputs = {}

    @classmethod
    def Field(cls, *args, **kwargs):
        if isinstance(cls._inputs, dict):
            for key in cls._inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {key: graphene.InputField(getattr(graphene, cls._inputs[key]))}
                )
        elif isinstance(cls._inputs, list):
            for key in cls._inputs:
                cls._meta.arguments["input"]._meta.fields.update({key: graphene.InputField(graphene.String)})

        if isinstance(cls._required_inputs, dict):
            for key in cls._required_inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {key: graphene.InputField(getattr(graphene, cls._required_inputs[key]), required=True)}
                )
        elif isinstance(cls._required_inputs, list):
            for key in cls._required_inputs:
                cls._meta.arguments["input"]._meta.fields.update(
                    {key: graphene.InputField(graphene.String, required=True)}
                )
        return super().Field(*args, **kwargs)


class ExtendedConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length


class RelayPermissionDjangoObjectType(DjangoObjectType, PermissionMixin):
    accessible = graphene.Boolean()
    global_privacy = graphene.String()

    class Meta:
        abstract = True

    def resolve_accessible(self, info):
        return True

    def resolve_global_privacy(self, info):
        return self.privacy.get("global")

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super().__init_subclass_with_meta__(**kwargs)

    @classmethod
    def get_queryset(cls, queryset, info):
        cls.check_permissions(info)
        return super().get_queryset(queryset, info)

    @classmethod
    def get_node(cls, info, id):
        obj = super().get_node(info, id)
        cls.check_object_permissions(info, obj)
        return obj


class SingleObjectParentMixin:
    parent_lookup_field: str = "pk"
    parent_lookup_url_kwarg = None
    check_parent_object_level_permission: bool = True
    parent_model = None
    parent_select_related_properties = None

    @classmethod
    def get_parent_queryset(cls):
        assert cls.parent_model is not None, (
            "You must define `parent_model` as class attribute in order to use " "`SingleObjectParentMixin`"
        )
        queryset = cls.parent_model.active_objects.all()
        if cls.parent_select_related_properties:
            assert isinstance(
                cls.parent_select_related_properties, (tuple, list)
            ), "`parent_select_related_properties` must be tuple or list"
            queryset = queryset.select_related(*cls.parent_select_related_properties)
        return queryset

    @classmethod
    def get_parent_object(cls, info, **kwargs):
        """
        Returns the parent object of the desired object the endpoint is modifying.
        """

        parent_lookup_url_kwarg = cls.parent_lookup_url_kwarg or cls.parent_lookup_field
        assert parent_lookup_url_kwarg in kwargs, (
            "Expected mutation %s to be called with an object keyword argument "
            'named "%s". Fix your argument conf, or set the `.parent_lookup_field` '
            "attribute on the mixin correctly." % (cls.__name__, parent_lookup_url_kwarg)
        )

        filter_kwargs = {cls.parent_lookup_field: kwargs.get(parent_lookup_url_kwarg, None)}
        parent_obj = get_object_or_404(cls.get_parent_queryset(), **filter_kwargs)

        # May raise a permission denied
        if cls.check_parent_object_level_permission:
            cls.check_object_permissions(info, parent_obj, **kwargs)

        return parent_obj


class SingleObjectMixin:
    lookup_field: str = "pk"
    lookup_url_kwarg = None
    check_object_level_permission: bool = True
    model = None
    select_related_properties = None

    @classmethod
    def get_queryset(cls):
        assert cls.model is not None, (
            "You must define `model` as class attribute in order to use " "`SingleObjectParentMixin`"
        )
        queryset = cls.model.objects.all()
        if cls.select_related_properties:
            assert isinstance(
                cls.select_related_properties, (tuple, list)
            ), "`select_related_properties` must be tuple or list"
            queryset = queryset.select_related(*cls.select_related_properties)
        return queryset

    @classmethod
    def get_object(cls, info, **kwargs):
        """
        Returns the object the endpoint is modifying.
        """

        lookup_url_kwarg = cls.lookup_url_kwarg or cls.lookup_field
        assert lookup_url_kwarg in kwargs, (
            "Expected mutation %s to be called with an object keyword argument "
            'named "%s". Fix your argument conf, or set the `.lookup_field` '
            "attribute on the mixin correctly." % (cls.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {cls.lookup_field: kwargs.get(lookup_url_kwarg, None)}
        obj = get_object_or_404(cls.get_queryset(), **filter_kwargs)

        # May raise a permission denied
        if cls.check_object_level_permission:
            cls.check_object_permissions(info, obj, **kwargs)

        return obj


class RemovePropertiesMixin:
    @classmethod
    def pop_properties(cls, actual_dictionary=None, properties=None):
        if isinstance(actual_dictionary, dict) and isinstance(properties, list):
            for prop in properties:
                actual_dictionary.pop(prop, None)


class BaseQueryChecker(PermissionMixin, SingleObjectMixin):
    lookup_url_kwarg: Optional[str] = None
    lookup_field: str = "pk"


class CreateNewJobMixin(Output):
    form = CreateJobForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        with transaction.atomic():
            f = cls.form(kwargs)

            if f.is_valid():
                job = f.save(commit=False)
                job.user = user
                job.save()
                return cls(success=True)
            else:
                return cls(success=False, errors=f.errors.get_json_data())


class UpdateJobMixin(Output):
    form = CreateJobForm

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        user = info.context.user
        job = cls.get_object(info, **kwargs)
        with transaction.atomic():
            f = cls.form(kwargs, instance=job, initial=model_to_dict(job))

            if f.is_valid():
                job = f.save()
                return cls(success=True, job=job)
            else:
                return cls(success=False, errors=f.errors.get_json_data())
