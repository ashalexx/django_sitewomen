from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost

menu = [{'title': "О Сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request):
    # загрузка всех данных через один запрос
    posts = Women.published.all().select_related('cat')
    # print(request.GET)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'women/index.html', context=data)


def handle_uploaded_file(f):
    with open(f'uploads/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'О Сайте',
                   'menu': menu,
                   'form': form})


def show_post(request, post_slug):
    # Пытается найти запись в модели Women по полю slug, равному post_slug
    # Если запись найдена — возвращает её
    # Если не найдена — автоматически вызывает Http404 (страница "Not Found")
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }

    return render(request, 'women/post.html', data)


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # try:
            #     # распаковка и сохранение в БД
            #     Women.objects.create(**form.cleaned_data)
            #     # перенаправляемся на главную страницу
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Ошибка добавления поста')
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', context=data)


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None
    }
    return render(request, 'women/index.html', context=data)
