
# Create your views here.
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from promanagement.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import PostForm, UserProfileForm, UserUpdateForm, CustomPasswordChangeForm, UserRegisterForm, PasswordChangeForm
from .models import UserProfile , Post, PostInteraction
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q


def home(request):
    posts = Post.objects.all()  # Get all posts for the home page
    return render(request, 'home.html', {'posts': posts})

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create a user object without saving yet
            user.first_name = form.cleaned_data.get('first_name')  # Save the first name
            user.last_name = form.cleaned_data.get('last_name')    # Save the last name
            user.save()  # Now save the user object
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # Redirect to home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # Redirect to the home page after logout
    return render(request, 'logout_confirm.html')  # Render the logout confirmation page


class PostListView(ListView):
    model = Post
    template_name = 'home.html'  # Template to render
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'object'

# Display post details
@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the user has liked or disliked the post
    user_liked = post.postinteraction_set.filter(user=request.user, interaction_type='like').exists()
    user_disliked = post.postinteraction_set.filter(user=request.user, interaction_type='dislike').exists()

    return render(request, 'post_detail.html', {
        'object': post,
        'user_liked': user_liked,
        'user_disliked': user_disliked,
        'user': request.user,
    })

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'  # Your template for creating posts
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)
    pass
    
#edit
class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'  # Reuse the post form template
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        # Get the post and check if the current user is the author
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        if post.author != self.request.user:
            return HttpResponseForbidden("You are not allowed to edit this post.")
        return post

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure the author is the logged-in user
        return super().form_valid(form)
    pass
    
#delete
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'  # Optional, since you are using a modal
    success_url = reverse_lazy('home')

    def get_queryset(self):
        # Ensure only the author can delete the post
        return self.model.objects.filter(author=self.request.user)
    pass

    
@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {
        'profile': profile,
        'user': request.user,
    })



@login_required
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update profile picture and bio
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        username_form = UserUpdateForm(request.POST, instance=request.user)

        if profile_form.is_valid() and username_form.is_valid():
            profile_form.save()
            username_form.save()
            messages.success(request, 'Your profile has been updated!')

            # Check if old password is provided for password change
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if old_password and new_password1 and new_password2:  # Password change fields were filled
                user = authenticate(username=request.user.username, password=old_password)
                if user is not None:
                    if new_password1 == new_password2:
                        request.user.set_password(new_password1)
                        request.user.save()
                        update_session_auth_hash(request, request.user)  # Keep the user logged in
                        messages.success(request, 'Your password has been updated!')
                    else:
                        messages.error(request, 'New passwords do not match.')
                else:
                    messages.error(request, 'Old password is incorrect.')

            return redirect('profile')

    else:
        profile_form = UserProfileForm(instance=profile)
        username_form = UserUpdateForm(instance=request.user)

    return render(request, 'edit_profile.html', {
        'profile_form': profile_form,
        'username_form': username_form,
    })
pass

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    interaction, created = PostInteraction.objects.get_or_create(user=request.user, post=post)

    if created:
        interaction.interaction_type = 'like'
        interaction.save()
    else:
        if interaction.interaction_type == 'like':
            interaction.delete()  # Remove like
        else:
            interaction.interaction_type = 'like'  # Change to like
            interaction.save()

    return redirect('post-detail', pk=post.pk)

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    interaction, created = PostInteraction.objects.get_or_create(user=request.user, post=post)

    if created:
        interaction.interaction_type = 'dislike'
        interaction.save()
    else:
        if interaction.interaction_type == 'dislike':
            interaction.delete()  # Remove dislike
        else:
            interaction.interaction_type = 'dislike'  # Change to dislike
            interaction.save()

    return redirect('post-detail', pk=post.pk)

class SearchView(ListView):
    model = Post
    template_name = 'search_results.html'  # Create this template
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print("Search query:", query)
        return Post.objects.filter(
            Q(title__icontains=query) | Q(category__name__icontains=query)
        )