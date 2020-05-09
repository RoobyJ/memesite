from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import random
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime, timezone
from .forms import CommentForm


class PostListView(ListView):
    model = Post
    template_name = 'main/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Posts'
    ordering = ['-post_published']
    paginate_by = 5

    #  this func is to replace the datetime format and give back a more user friendly format
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        for post in posts:
            temp = datetime.now(timezone.utc) - post.post_published
            time_difference = temp.total_seconds()
            if time_difference < 59:
                post.post_published = 'just now'
            elif 59 < time_difference < 3599:
                post.post_published = f'{int(time_difference / 60)} minutes ago'
            elif 3599 < time_difference < 86399:
                post.post_published = f'{int(time_difference / 3600)} hours ago'
            elif 86399 < time_difference < 604799:
                if 86399 < time_difference < 172799:
                    post.post_published = 'a day ago'
                elif 172799 < time_difference < 259199:
                    post.post_published = 'two days ago'
                elif 259199 < time_difference < 345599:
                    post.post_published = 'three days ago'
                elif 345599 < time_difference < 431999:
                    post.post_published = 'four days ago'
                elif 431999 < time_difference < 518399:
                    post.post_published = 'fifth days ago'
                elif 518399 < time_difference < 604799:
                    post.post_published = 'six days ago'
            elif 604799 < time_difference < 2419199:
                if 604799 < time_difference < 1209599:
                    post.post_published = 'a week ago'
                elif 1209599 < time_difference < 1814399:
                    post.post_published = 'two weeks ago'
                elif 1814399 < time_difference < 2419199:
                    post.post_published = 'three weeks ago'
            elif 2591999 < time_difference < 5183999:
                post.post_published = 'a month ago'
            elif 5183999 < time_difference < 7775999:
                post.post_published = 'two months ago'
            elif 7775999 < time_difference < 15551999:
                post.post_published = 'six months ago'
            elif 15551999 < time_difference < 31103999:
                post.post_published = ' a year ago'
            elif 31103999 < time_difference:
                post.post_published = 'long ago'

        p = Paginator(posts, self.paginate_by)
        context['Posts'] = p.page(context['page_obj'].number)
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Posts'
    paginate_by = 5

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = Post.objects.filter(created_by=user).order_by('-post_published')
        #  this func is to replace the datetime format and give back a more user friendly format
        for post in posts:
            post.post_published = datetime.now(timezone.utc) - post.post_published
            time_difference = post.post_published.total_seconds()
            if time_difference < 59:
                post.post_published = 'just now'
            elif 59 < time_difference < 3599:
                post.post_published = f'{int(time_difference / 60)} minutes ago'
            elif 3599 < time_difference < 86399:
                post.post_published = f'{int(time_difference / 3600)} hours ago'
            elif 86399 < time_difference < 604799:
                if 86399 < time_difference < 172799:
                    post.post_published = 'a day ago'
                elif 172799 < time_difference < 259199:
                    post.post_published = 'two days ago'
                elif 259199 < time_difference < 345599:
                    post.post_published = 'three days ago'
                elif 345599 < time_difference < 431999:
                    post.post_published = 'four days ago'
                elif 431999 < time_difference < 518399:
                    post.post_published = 'fifth days ago'
                elif 518399 < time_difference < 604799:
                    post.post_published = 'six days ago'
            elif 604799 < time_difference < 2419199:
                if 604799 < time_difference < 1209599:
                    post.post_published = 'a week ago'
                elif 1209599 < time_difference < 1814399:
                    post.post_published = 'two weeks ago'
                elif 1814399 < time_difference < 2419199:
                    post.post_published = 'three weeks ago'
            elif 2591999 < time_difference < 5183999:
                post.post_published = 'a month ago'
            elif 5183999 < time_difference < 7775999:
                post.post_published = 'two months ago'
            elif 7775999 < time_difference < 15551999:
                post.post_published = 'six months ago'
            elif 15551999 < time_difference < 31103999:
                post.post_published = ' a year ago'
            elif 31103999 < time_difference:
                post.post_published = 'long ago'

        return posts


def post_detail(request, **kwargs):
    template_name = 'main/post_detail.html'
    post = get_object_or_404(Post, id=kwargs['pk'])
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.comment_author = post.created_by
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'object': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'post_username': post.created_by.username})


# Enables the user to create a post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['post_title', 'post_content', 'post_image']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['post_title', 'post_content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# gives back a random post
def random_request(request):
    return render(request=request,
                  template_name='main/random.html',
                  context={'Post': Post.objects.get(id=random.randint(1, len(Post.objects.values_list('id'))))
                           })
