import graphene

from core.schema import OpenIMISMutation


class PublicServiceInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    title = graphene.String(requred=False)
    description = graphene.String(required=False)
    is_active = graphene.Boolean(required=False)
