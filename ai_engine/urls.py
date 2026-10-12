from django.urls import path

from .views import generate_questions,profile


urlpatterns = [
    path(
        "generate-questions/",
        generate_questions,
        name="generate_questions"
    ),
    path("profile/", profile),
]