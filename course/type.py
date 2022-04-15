import graphene
from graphene_file_upload.scalars import Upload


class CourseInput(graphene.InputObjectType):
    name = graphene.NonNull(graphene.String)
    user = graphene.List(graphene.Int,required = False)
    teacher = graphene.NonNull(graphene.Int)

class AssignmentInput(graphene.InputObjectType):
    title = graphene.NonNull(graphene.String)
    course = graphene.Int()

class SubmissionInput(graphene.InputObjectType):
    assignment = graphene.NonNull(graphene.Int)
    user = graphene.NonNull(graphene.Int)
    file = Upload()