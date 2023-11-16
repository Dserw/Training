from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Post, Comment
from .filters import PostFilter
from .forms import PostForm, CommentForm
from .signals import my_handler

# Create your views here.


class PostsList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 4


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('posts.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create.html'


class CreateComment(PermissionRequiredMixin, CreateView):
    permission_required = ('comments.add_comment',)
    raise_exception = True
    model = Comment
    form_class = CommentForm
    template_name = 'create_comment.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.commentPost = Post.objects.get(pk=self.kwargs['pk'])
        self.success_url = reverse_lazy('post', kwargs={'pk': form.instance.commentPost.pk})

        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('posts.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'update.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('posts.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts')


class CommentsListUser(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments_user.html'
    context_object_name = 'comments_user'
    paginate_by = 6

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(commentPost=post)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context


class CommentDetail(DetailView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'


class CommentAccept(View):
    model = Comment
    template_name = 'comment_accept.html'
    context_object_name = 'comment_accept'

    def get(self, request, id_comment):
        comment = get_object_or_404(Comment, id=id_comment)
        comment.status = not comment.status
        comment.save()
        post_url = reverse('post', kwargs={'pk': comment.commentPost.pk})

        return HttpResponseRedirect(post_url)


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('posts')


