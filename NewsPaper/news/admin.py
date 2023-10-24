
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, Group
from modeltranslation.admin import TranslationAdmin
from .models import *
# Register your models here.


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(PostCategory)


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post

class SubscriberInline(admin.TabularInline):
    model = Subscriber
    extra = 1  # Количество дополнительных полей для отображения

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubscriberInline]  # Добавляем инлайн для Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')

