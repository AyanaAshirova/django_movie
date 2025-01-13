from django import forms

from .models import Comment


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'сols': 120,
                'rows': 40,
                'placeholder': 'Enter your comment here..'
            }),
        }

