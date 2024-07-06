from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateBoxView.as_view(), name='create_boxes'),
    path('update/<uuid:pk>/', UpdateBoxView.as_view(), name='update_boxes'),
    path('list/', ListAllBoxesView.as_view(), name='list_boxes'),
    path('list-user-boxes/', ListUserBoxesView.as_view(), name='list_user_boxes'),
    path('delete/<uuid:pk>/', DeleteBoxView.as_view(), name='delete_boxes'),
    path("*", PageNotFound.as_view(), name='page_not_found')
]
