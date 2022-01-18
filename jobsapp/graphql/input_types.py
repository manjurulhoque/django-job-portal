import graphene


class TagInput(graphene.InputObjectType):
    pk = graphene.Int()
