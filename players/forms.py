from django.forms import ModelForm
from players.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
