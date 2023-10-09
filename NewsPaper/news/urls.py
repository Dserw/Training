from django.urls import path
# Импортируем созданное нами представление
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [

   path('', PostsList.as_view(), name='news'),
   path('<int:pk>', PostDetail.as_view(), name='news_detail'),
   path('search/', SearchPost.as_view(), name='news_search'),
   path('news/create', NewsCreate.as_view(), name='news_create'),
   path('articles/create', ArticlesCreate.as_view(), name='articles_create'),
   path('<int:pk>/edit', NewsUpdate.as_view(), name='news_edit'),
   path('articles/<int:pk>/edit', ArticlesUpdate.as_view(), name='articles_edit'),
   path('<int:pk>/delete', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete', ArticlesDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>', CategoryList.as_view(), name='category_list')

]


