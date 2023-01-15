from django.urls import path
from phil_1 import views


urlpatterns = [
	path("form/", views.index),
    path("form/create/", views.create),
    path("form/find_person/", views.find_person),
    path("form/edit/<int:id>", views.edit),
    path("form/delete/<int:id>/", views.delete),
    path("form/delete_all/", views.delete_all),
    path("form/register/", views.register),
    path("form/quit/", views.quit),
    path("form/upload/", views.upload),
    path("form/export_all/", views.export_all),
    path("form/export_data_from_find_person/", views.export_data_from_find_person)
]