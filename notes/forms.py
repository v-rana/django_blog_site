from django import forms
from .models import Notes


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title' , 'text')
    

    
    def clean_title(self):
        title = self.cleaned_data['title']

        if 'fk' in title:
            raise forms.ValidationError('title contains inappropriate word')

        return title