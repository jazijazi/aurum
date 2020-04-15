from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('subject', 'text')
        #widgets = {'user': forms.HiddenInput() , 'product': forms.HiddenInput() }