from django.urls import path
from . import views

urlpatterns = [
    path('show_data/<int:id>', views.show_data, name='show_data')
]