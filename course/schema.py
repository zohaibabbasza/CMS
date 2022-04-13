import graphene
from course import models
from course.type import CourseInput
from users.schema import UserType

class CourseType(graphene.ObjectType):
    id = graphene.NonNull(graphene.Int)
    name = graphene.NonNull(graphene.String)
    user = graphene.List(UserType)
    teacher = graphene.Field(UserType)

    def resolve_user(course, *args, **kwargs):
        return course.user.all()

    def resolve_teacher(course,*args,**kwargs):
        return course.teacher

class Query(graphene.ObjectType):
    courses = graphene.List(CourseType)

    def resolve_courses(self, info, **kwargs):
        return models.Course.objects.all()

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

class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()