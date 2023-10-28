from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)


class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostCategory)

