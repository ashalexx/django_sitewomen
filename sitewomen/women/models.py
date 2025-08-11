from tkinter.font import names

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Новый менеджер записей
class PublishedManager(models.Manager):
    def get_queriset(self):
        return super().get_queriset(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    # Свое перечисление, 'понятное'
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    photo = models.ImageField(upload_to='photos/%y/%m/%d/', default=None, blank=True, null=True, verbose_name='Фото')
    content = models.TextField(blank=True, verbose_name='Контент')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Тэг')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='wuman',
                                   verbose_name='Муж')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # сохраняем slug не вводя его отдельно поле !НЕ работает с русским алфавитом
    # можно исправить костылем - словарем возврата русских-англ букв
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     # вызываем базовый класс и метод save()
    #     super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
