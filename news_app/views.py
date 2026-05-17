from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .forms import RegisterForm, UserUpdateForm, NewsForm
from .models import News


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! Регистрация прошла успешно.')
            return redirect('home')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'С возвращением, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль был обновлен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        'user_news_count': News.objects.filter(author=request.user).count()
    }
    return render(request, 'profile.html', context)


@login_required
def profile_delete_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Ваш аккаунт был успешно удален.')
        return redirect('home')
    return render(request, 'profile_confirm_delete.html')


def home_view(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 5)  # 5 news per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})


def news_detail_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    is_author = False
    if request.user.is_authenticated:
        is_author = (news.author == request.user)
    return render(request, 'news_detail.html', {'news': news, 'is_author': is_author})


@login_required
def news_create_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость успешно создана!')
            return redirect('news_detail', pk=news.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = NewsForm()
    return render(request, 'news_form.html', {'form': form, 'title': 'Создать новость'})


@login_required
def news_edit_view(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Check if user is the author
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать эту новость")

    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость успешно обновлена!')
            return redirect('news_detail', pk=news.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = NewsForm(instance=news)

    return render(request, 'news_form.html', {'form': form, 'title': 'Редактировать новость'})


@login_required
def news_delete_view(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Check if user is the author
    if news.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить эту новость")

    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость успешно удалена!')
        return redirect('home')

    return render(request, 'news_confirm_delete.html', {'news': news})  # ИСПРАВЛЕНО: news вместо news_123