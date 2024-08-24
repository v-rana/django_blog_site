from django.contrib import admin

from . models import Notes 
class NotesAdmin(admin.ModelAdmin):
    list_display = ("title", "text", "created")

admin.site.register(Notes, NotesAdmin)
# Register your models here.
