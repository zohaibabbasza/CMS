from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    user = models.ManyToManyField(User)
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name='teacher')

    def __str__(self) -> str:
        return self.name

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    file = models.FileField(null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title + ' | ' + self.user.email
