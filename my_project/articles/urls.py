from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet
from .views import register, profile_view, article_list, article_detail, save_article, remove_saved_article, saved_articles, add_article, edit_article, edit_comment, delete_comment, like_comment, dislike_comment
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', article_list, name='article_list'),

    path("register/", register, name="registration"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/', profile_view, name='profile'),

    path('article/api/', include(router.urls)),

    path('add/', add_article, name='add_article'),
    path('edit/<int:article_id>/', edit_article, name='edit_article'),
    path('article/<int:pk>/', article_detail, name='article_detail'),
    path('articles/save/<int:article_id>/', save_article, name='save_article'),
    path('articles/remove_saved/<int:saved_article_id>/', remove_saved_article, name='remove_saved_article'),
    path('articles/saved/', saved_articles, name='saved_articles'),

    path('comment/edit/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('comment/like/<int:comment_id>/', like_comment, name='like_comment'),
    path('comment/dislike/<int:comment_id>/', dislike_comment, name='dislike_comment'),
]
