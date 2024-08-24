

from django.shortcuts import render
from django.db.models.query import QuerySet
from django.views.generic.edit import DeleteView
from django.views.generic import ListView, DetailView , CreateView , UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from .forms import NotesForm
from .models import Notes

"""Class view to list all the notes"""
class NotesListView(ListView):
    model = Notes
    context_object_name = 'notes'
    template_name = 'notes_list.html'
    paginate_by = 2
    ordering = ['-created']

"""Class view to display details of a single note on the basis of the note id"""
class NotesDetailView(DetailView):
    model = Notes
    context_object_name = 'note'
    template_name = 'notes_detail.html'

"""Class view to create a new note"""
class NotesCreateView(LoginRequiredMixin,CreateView):
    model = Notes
    form_class = NotesForm
    template_name = 'notes_create.html'
    success_url = '/notes'
    login_url = '/login'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return  HttpResponseRedirect(self.get_success_url())
    
"""Class view to update an existing note"""
class NotesUpdateView(LoginRequiredMixin,UpdateView):
    model = Notes
    form_class = NotesForm
    template_name = 'notes_create.html'
    success_url = '/notes'
    login_url = '/login'   
    def get_object(self, queryset=None):
        note = super().get_object(queryset)
        if note.user != self.request.user:
            raise PermissionDenied("You are not allowed to edit this note.")
        return note


"""Class view to delete an existing note"""
class NotesDeleteView(LoginRequiredMixin,DeleteView):
    model = Notes
    template_name = 'notes_delete.html'
    success_url = '/notes'
    login_url = '/login'
    def get_object(self, queryset=None):
        note = super().get_object(queryset)
        if note.user != self.request.user:
            raise PermissionDenied("You are not allowed to delete this note.")
        return note