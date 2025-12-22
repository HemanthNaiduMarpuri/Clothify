from django.urls import path
from .views import CommentView, comment_like, comment_dislike, delete_comment

urlpatterns = [
    path('<int:pk>/', CommentView.as_view(), name='comment'),
    path('<int:id>/like/', comment_like, name='comment_like'),
    path('<int:id>/dislike/', comment_dislike, name='comment_dislike'),
    path('<int:id>/delete/', delete_comment, name='delete_comment')
]
