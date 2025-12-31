import django_filters as filters
from django import forms
from django.utils.translation import gettext_lazy as _

from application.models import Item, ItemQuerySet


class ItemFilter(filters.FilterSet):
    q = filters.CharFilter(
        method="search",
        widget=forms.TextInput(
            attrs={
                "placeholder": _("search"),
            },
        ),
    )

    def search(self, queryset: ItemQuerySet, _: str, value: str) -> ItemQuerySet:
        if not value.strip():
            return queryset

        return queryset.search(value)

    class Meta:
        model = Item
        fields = ("q",)
