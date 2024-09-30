from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostDetailView, PostCreateView, PostEditView, PostDeleteView, profile_view, edit_profile_view , like_post, dislike_post, SearchView
from . import views
from .views import PostCreateView
from .views import login_view, logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
     path('', views.home, name='home'),
     path('login/', login_view, name='login'),
     path('logout/', logout_view, name='logout'), 
     path('register/', views.register, name='register'),
     path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
     path('post/create/', PostCreateView.as_view(), name='post-create'),
     path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),  # Edit path
     path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete path
     path('profile/', profile_view, name='profile'),
     path('profile/edit/', edit_profile_view, name='edit_profile'),
     path('post/<int:pk>/like/', like_post, name='like-post'),
     path('post/<int:pk>/dislike/', dislike_post, name='dislike-post'),
     path('search/', SearchView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
