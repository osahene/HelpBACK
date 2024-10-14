import graphene
import account.schema 

class Query(account.schema.Query, graphene.ObjectType):
    pass


class Mutation(account.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)