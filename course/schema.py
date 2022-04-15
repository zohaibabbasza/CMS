import graphene
from course import models
from course.type import CourseInput,AssignmentInput,SubmissionInput
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload

class CourseType(DjangoObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = models.Course
        filter_fields = {
            'id','name'
        }
        interfaces = (graphene.relay.Node, )

class AssignmentType(DjangoObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = models.Assignment
        filter_fields = {
            'id','title','course'
        }
        interfaces = (graphene.relay.Node, )

class SubmissionType(DjangoObjectType):
    id = graphene.ID(source='id', required=True)
    class Meta:
        model = models.Submission
        filter_fields = {
            'id'
        }
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    course = graphene.relay.Node.Field(CourseType)
    all_courses = DjangoFilterConnectionField(CourseType)
    assignment = graphene.relay.Node.Field(AssignmentType)
    all_assignments =  DjangoFilterConnectionField(CourseType)
    submission = graphene.relay.Node.Field(SubmissionType)
    all_submissions =  DjangoFilterConnectionField(SubmissionType)


class CreateCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        course_data = CourseInput(required=True)

    def mutate(self, info, course_data):
        course_data['teacher'] = models.User.objects.get(id=course_data['teacher'])
        users = models.User.objects.filter(id__in=course_data.pop('user'))
        course = models.Course.objects.create(
            **course_data
        )
        course.user.set(users)
        return CreateCourse(course=course)  

class CreateAssignment(graphene.Mutation):
    assignment = graphene.Field(AssignmentType)

    class Arguments:
        assignment_data = AssignmentInput(required=True)

    def mutate(self,info,assignment_data):
        assignment_data['course'] = models.Course.objects.get(id=assignment_data['course'])
        assignment = models.Assignment.objects.create(
            **assignment_data
        )
        return CreateAssignment(assignment=assignment)

class UpdateAssignment(graphene.Mutation):
    assignment = graphene.Field(AssignmentType)

    class Arguments:
        id = graphene.NonNull(graphene.Int)
        title = graphene.String()
        course = graphene.Int()

    def mutate(self,info,id,title=None,course=None):
        assignment = models.Assignment.objects.get(id=id)
        assignment.title = title if title is not None else assignment.title
        assignment.course = models.Course.objects.get(id=course) if course is not None else assignment.course
        assignment.save()
        return UpdateAssignment(assignment=assignment)

class DeleteAssignment(graphene.Mutation):
    assignment = graphene.Field(AssignmentType)

    class Arguments:
        id = graphene.NonNull(graphene.Int)

    def mutate(self,info,id):
        assignment = models.Assignment.objects.get(id=id)
        if assignment is not None:
            assignment.delete()
        return DeleteAssignment(assignment=assignment)

class CreateSubmission(graphene.Mutation):
    submission = graphene.Field(SubmissionType)

    class Arguments:
        submission_data = SubmissionInput(required=True)

    def mutate(self,info,submission_data):
        submission_data['assignment'] = models.Assignment.objects.get(id=submission_data['assignment'])
        submission = models.Assignment.objects.create(
            **submission_data
        )
        return CreateSubmission(submission=submission)

class UpdateSubmission(graphene.Mutation):
    submission = graphene.Field(SubmissionType)

    class Arguments:
        id = graphene.NonNull(graphene.Int)
        file = Upload()

    def mutate(self,info,id,file=None):
        submission = models.Submission.objects.get(id=id)
        submission.file = file if file is not None else submission.file
        submission.save()
        return UpdateSubmission(submission=submission)

class DeleteSubmission(graphene.Mutation):
    submission = graphene.Field(SubmissionType)

    class Arguments:
        id = graphene.NonNull(graphene.Int)

    def mutate(self,info,id):
        submission = models.Submission.objects.get(id=id)
        if submission is not None:
            submission.delete()
        return DeleteSubmission(submission=submission)

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    create_assignment = CreateAssignment.Field()
    update_assignment = UpdateAssignment.Field()
    delete_assignment = DeleteAssignment.Field()
    create_submission = CreateSubmission.Field()
    update_submission = UpdateSubmission.Field()
    delete_submission = DeleteSubmission.Field()