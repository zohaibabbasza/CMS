import graphene

class CourseInput(graphene.InputObjectType):
    name = graphene.NonNull(graphene.String)
    user = graphene.List(graphene.Int,required = False)
    teacher = graphene.NonNull(graphene.Int)