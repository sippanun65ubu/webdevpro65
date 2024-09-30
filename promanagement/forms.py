from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from promanagement.models import Post ,Category, UserProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data
    
class PostForm(forms.ModelForm):
    new_category = forms.CharField(required=False, max_length=100, label="New Category")

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()  # Load existing categories
        self.fields['title'].widget.attrs.update({'class': 'border rounded-lg p-2 w-full'})
        self.fields['content'].widget.attrs.update({'class': 'border rounded-lg p-2 w-full', 'rows': 5})
        self.fields['image'].widget.attrs.update({'class': 'border rounded-lg p-2 w-full'})
        self.fields['category'].widget.attrs.update({'class': 'border rounded-lg p-2 w-full'})

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)

        # Check if a new category is provided
        new_category = self.cleaned_data.get('new_category')
        if new_category:
            category, created = Category.objects.get_or_create(name=new_category)
            post.category = category

        if commit:
            post.save()
        return post
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password']