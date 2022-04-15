from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', FileUploadGraphQLView.as_view(graphiql=True)),

]