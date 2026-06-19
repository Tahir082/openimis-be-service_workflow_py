import graphene
from graphene_django import DjangoObjectType

from core.gql_queries import InteractiveUserGQLType
from .models import *
from core import prefix_filterset, ExtendedConnection
from location.schema import LocationGQLType
import django_filters
from graphql_relay.node.node import from_global_id


class PublicServiceGQLType(DjangoObjectType):
    class Meta:
        model = PublicService
        interfaces = (graphene.relay.Node,)
        filter_fields = {
            "id": ["exact"],
            "title": ["exact", "icontains"],
            "description": ["exact", "icontains"],
            "is_active": ["exact"],
        }