from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Exists, OuterRef
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_protect

from .filters import PostFilter
from .models import Post, Category, PostCategory
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .forms import ArticleForm, NewsForm
from django.utils.translation import gettext as _
# Create your views here.


class PostsList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
            return obj


class SearchPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    filterset_class = PostFilter


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    template_name = 'articles_create.html'

    def get(self, request):
        form = NewsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.type = 'AR'
            news.save()
            category_id = request.POST.get('category')
            if category_id:
                category = Category.objects.get(pk=category_id)
                PostCategory.objects.create(postThrough=news, categoryThrough=category)

            return HttpResponseRedirect('/news/')
        return render(request, self.template_name, {'form': form})


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    template_name = 'news_create.html'

    def get(self, request):
        form = NewsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.type = 'NW'
            news.save()
            category_id = request.POST.get('category')
            if category_id:
                category = Category.objects.get(pk=category_id)
                PostCategory.objects.create(postThrough=news, categoryThrough=category)

            return HttpResponseRedirect('/news/')
        return render(request, self.template_name, {'form': form})


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    queryset = Post.objects.filter(type='NW')
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news')


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    queryset = Post.objects.filter(type='AR')
    template_name = 'articles_edit.html'
    success_url = reverse_lazy('news')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

    def get_queryset(self):
        return super().get_queryset().filter(type='NW')


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('news')
    def get_queryset(self):
        return super().get_queryset().filter(type='AR')


class CategoryList(PostsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

