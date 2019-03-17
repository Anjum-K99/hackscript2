from django import forms
from .models import Document,Comment

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document',)

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','email','comment',)