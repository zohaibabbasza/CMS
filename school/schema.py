import graphene
import graphql_jwt
import users.schema
from course.schema import Query as courses_query
from course.schema import Mutation as course_mutation

class Query(users.schema.Query, 
            courses_query,graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation,
                course_mutation, graphene.ObjectType,):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)