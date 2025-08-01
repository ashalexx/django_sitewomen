from django.contrib import admin, messages

from .models import Women, Category


# создаем собственный фильтр на панели фильтров
class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус у женщин'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'married':
            return queryset.filter(husband__isnull=False)
        else:
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # отображение
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    # кликабельность
    list_display_links = ('title',)
    # сортировка
    ordering = ['title', 'time_create', 'is_published', 'cat']
    # возможность менять не заходя
    list_editable = ['is_published']
    # макс кол-во статей отображаемых на одной странице
    list_per_page = 3
    actions = ['set_published', 'set_druft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']

    # создаем собственное поле отображаемое в админпанели
    # с отображением на русском языке за счет декоратора
    # и сортировкой по контенту
    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, women: Women):
        return f'Описание {len(women.content)} символов'

    # новый атрибут действия в выпадающем меню
    @admin.display(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Опубликовано {count} записей.')

    @admin.display(description='Снять с публикации выбранные записи')
    def set_druft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} записей.', messages.WARNING)


# admin.site.register(Women, WomenAdmin)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # отображение
    list_display = ('id', 'name')
    # кликабельность
    list_display_links = ('id', 'name')
