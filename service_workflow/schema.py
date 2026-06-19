import os
from collections import defaultdict

import graphene
import graphene_django_optimizer as gql_optimizer
import requests
from django.db.models import Count
from django.db.models import F
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext as _
from graphene.types.generic import GenericScalar
from graphql import GraphQLError

from core.models.user import InteractiveUser
from core.models.user import UserRole
from core.schema import OrderedDjangoFilterConnectionField
from .gql_mutations import *
from .gql_queries import *
from .models import *
from .services.public_service_services import PublicServiceServices
from django.db.models.expressions import RawSQL


class Query(graphene.ObjectType):
    public_service = OrderedDjangoFilterConnectionField(
        PublicServiceGQLType,
        client_mutation_id=graphene.String(),
        orderBy=graphene.List(of_type=graphene.String),
    )


    def resolve_public_service(self, info, **kwargs):
        service = PublicServiceServices(info.context.user)
        query = service.get(**kwargs)
        return gql_optimizer.query(query, info)




class Mutation(graphene.ObjectType):
    create_public_service = CreatePublicServiceMutation.Field()
    update_public_service = UpdatePublicServiceMutation.Field()
    delete_public_service = DeletePublicServiceMutation.Field()

