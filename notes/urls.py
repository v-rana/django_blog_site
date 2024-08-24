from django.urls import path 

from . import views

urlpatterns = [
    path('notes', views.NotesListView.as_view(), name='notes_list'),
    path('notes/<int:pk>', views.NotesDetailView.as_view(), name='notes_detail'),
    path('notes/<int:pk>/edit', views.NotesUpdateView.as_view(), name='notes_update'),
    path('notes/create', views.NotesCreateView.as_view(), name='notes_create'),
    path('notes/<int:pk>/delete', views.NotesDeleteView.as_view(), name='notes_delete'),
]