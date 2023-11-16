from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/comment/', CreateComment.as_view(), name='create_comment'),
    path('comments_user/<int:pk>/', CommentsListUser.as_view(), name='comments_user'),
    path('comment/<int:pk>/', CommentDetail.as_view(), name='comment'),
    path('comment_delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),
    path('accept/<int:id_comment>/', CommentAccept.as_view(), name='comment_accept'),
]
