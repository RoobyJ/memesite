from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views


app_name = 'main'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('random/', views.random_request, name='random'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
