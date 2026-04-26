import json
import os
from datetime import date
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import NewsForm


DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'news.json')


def ensure_data_file_exists():
    data_dir = os.path.dirname(DATA_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_news():
    ensure_data_file_exists()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            news_list = json.load(f)
            news_list.sort(key=lambda x: x.get('date', ''), reverse=True)
            return news_list
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_news(news_list):
    ensure_data_file_exists()
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)


def get_next_id(news_list):
    if not news_list:
        return 1
    max_id = max(news.get('id', 0) for news in news_list)
    return max_id + 1


def home_view(request):
    news_list = load_news()
    today = date.today().isoformat()

    for news in news_list:
        news['is_today'] = (news.get('date') == today)

    context = {
        'news_list': news_list,
        'page_title': 'Главная страница',
    }
    return render(request, 'home.html', context)


def news_detail_view(request, news_id):
    news_list = load_news()

    news_item = None
    for news in news_list:
        if news.get('id') == news_id:
            news_item = news
            break

    if news_item is None:
        raise Http404(f"Новость с ID {news_id} не найдена")

    context = {
        'news': news_item,
        'page_title': news_item.get('title', 'Новость'),
    }
    return render(request, 'news_detail.html', context)


def add_news_view(request):

    if request.method == 'POST':
        form = NewsForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            summary = form.cleaned_data['summary']
            content = form.cleaned_data['content']

            news_date = form.cleaned_data['date']
            if not news_date:
                news_date = date.today()

            news_list = load_news()
            new_id = get_next_id(news_list)

            new_news = {
                'id': new_id,
                'title': title,
                'summary': summary,
                'content': content,
                'date': news_date.isoformat() if hasattr(news_date, 'isoformat') else str(news_date)
            }

            news_list.append(new_news)
            save_news(news_list)

            return redirect('success')
    else:
        form = NewsForm()

    context = {
        'form': form,
        'page_title': 'Добавить новость',
    }
    return render(request, 'add_news.html', context)


def success_view(request):
    context = {
        'page_title': 'Новость добавлена',
        'message': 'Ваша новость успешно опубликована!'
    }
    return render(request, 'success.html', context)