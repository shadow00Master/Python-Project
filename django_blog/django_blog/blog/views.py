from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment
from .forms import PostForm, CommentForm, RegisterForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        # Handle a new comment being submitted on the detail page
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            messages.success(request, "Comment added.")
            return redirect('post_detail', pk=self.object.pk)
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published.")
        return super().form_valid(form)


class AuthorRequiredMixin(UserPassesTestMixin):
    """Only the post's author can edit or delete it."""

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Post updated.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        messages.success(self.request, "Post deleted.")
        return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account was created.")
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
