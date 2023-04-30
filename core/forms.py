from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...'}
