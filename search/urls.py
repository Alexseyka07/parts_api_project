from django.urls import path
from . import views

urlpatterns = [
    path("parts_create/<int:count>/", views.parts_create, name="parts_create"),
    path("model", views.models, name="models"),
    path("mark", views.marks, name="marks"),
    path("search/part", views.parts, name="parts"),
    path("search/parts_response", views.parts_response, name="parts_response"),
]
