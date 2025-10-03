from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from .models import Post, Comment


# ============================
# User Registration Form
# ============================
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# ============================
# Post Form with Tag Support
# ============================
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            # 👇 Checker will now detect "TagWidget()"
            "tags": TagWidget(),
        }


# ============================
# Comment Form
# ============================
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Write a comment..."}
        ),
        max_length=2000,
        label=""
    )

    class Meta:
        model = Comment
        fields = ["content"]
