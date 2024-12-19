from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)  # 댓글 텍스트 필드만 포함

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)  # 대댓글 텍스트 필드만 포함
