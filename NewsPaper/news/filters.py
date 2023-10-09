from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, CharFilter
from .models import Category


class PostFilter(FilterSet):

    category = ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='All'
    )

    name = CharFilter(
        field_name='head',
        lookup_expr='icontains',
        label='Название'
    )

    date = DateTimeFilter(
        field_name='date_create',
        lookup_expr='lt',
        label='Дата',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'}
        )
    )

