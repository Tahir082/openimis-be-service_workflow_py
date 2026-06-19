import graphene

from core.schema import OpenIMISMutation


class PublicServiceInputType(OpenIMISMutation.Input):
    id = graphene.String(required=False)
    title = graphene.String(requred=True)
    description = graphene.String(required=True)
    is_active = graphene.Boolean(required=True)
