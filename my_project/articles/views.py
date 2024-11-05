from django.urls import reverse
from rest_framework import viewsets, permissions
from .models import Article, Comment, Profile, SavedArticle
from .serializers import ArticleSerializer, CommentSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleForm, CommentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from .utils import send_notification_email
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
               
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def article_list(request):
    articles = Article.objects.all()

    # Сортировка
    sort_by = request.GET.get('sort_by')
    if sort_by == 'date':
        articles = articles.order_by('-date_published')
    elif sort_by == 'author':
        articles = articles.order_by('author__user__username')
    elif sort_by == 'tags':
        articles = articles.order_by('tags')

    # Поиск
    query = request.GET.get('q')
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    return render(request, 'article_list.html', {'articles': articles, 'query': query, 'sort_by': sort_by})


@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    profile = get_object_or_404(Profile, user=request.user)
    comments = article.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article  
            comment.author = profile
            comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'form': form,
    }
    return render(request, 'article_detail.html', context)


@login_required
def add_comment(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        text = request.POST.get('text')
        try:
            comment = Comment.objects.create(
                user=request.user,
                article=article,
                text=text
            )
            comment.save()
            send_notification_email(article.author_id.email, article.title, comment.text)
            messages.success(request, 'Комментарий добавлен!')
        except Exception as e:
            logger.error(f'Error adding comment: {e}')
            messages.error(request, 'Произошла ошибка при добавлении комментария.')
        return redirect('article_detail', article_id=article.id)


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user.profile != comment.author:
        return redirect('profile') 
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'articles/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user.profile != comment.author_id:
        messages.error(request, "Вы не можете удалить этот комментарий.")
        return redirect('profile')

    comment.delete()
    messages.success(request, "Комментарий успешно удален.")
    return redirect('profile')


@login_required
def save_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    profile = get_object_or_404(Profile, user=request.user)

    if article in profile.saved_articles.all():
        profile.saved_articles.remove(article)
        message = "Статья удалена из избранного."
    else:
        profile.saved_articles.add(article)
        message = "Статья добавлена в избранное."

    profile.save()
    return redirect('article_detail', pk=article.id)


@login_required
def remove_saved_article(request, saved_article_id):
    profile = get_object_or_404(Profile, user=request.user)
    saved_article = get_object_or_404(SavedArticle, id=saved_article_id, user=profile)
    saved_article.delete()
    return redirect('saved_articles')


@login_required
def saved_articles(request):
    profile = get_object_or_404(Profile, user=request.user)
    saved_articles = SavedArticle.objects.filter(user=profile).select_related('article')
    return render(request, 'saved_articles.html', {'saved_articles': saved_articles})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('article_list')  # перенаправление после успешного входа
        else:
            messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("article_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author_id = Profile.objects.get(user=request.user)
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'add_article.html', {'form': form})


@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect(reverse('article_detail', kwargs={'pk': article_id}))
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form, 'article': article})


def like_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.likes += 1
        comment.save()
        return JsonResponse({'likes': comment.likes})


def dislike_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        comment.dislikes += 1
        comment.save()
        return JsonResponse({'dislikes': comment.dislikes})
    

@login_required
def profile_view(request):
    profile = request.user.profile
    saved_articles = profile.saved_articles.all()

    context = {
        'saved_articles': saved_articles,
    }
    return render(request, 'profile.html', context)