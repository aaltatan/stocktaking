from django.db import models
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _


def get_keywords_query(
    value: str,
    *,
    field_name: str = "search",
) -> models.Q:
    """Return a search query."""
    query: models.Q = models.Q()
    keywords = value.split(" ")

    for word in keywords:
        kwargs = {f"{field_name}__icontains": word}
        query &= models.Q(**kwargs)

    return query


def concat_fields(*fields: str, repeat: int = 2) -> Concat:
    if len(fields) <= 1:
        message = "Expected at least two fields, got one!"
        raise ValueError(message)

    concatenated_fields: list[models.F | models.Value] = []

    for field in fields:
        concatenated_fields.append(models.F(field))
        concatenated_fields.append(models.Value(" "))

    return Concat(*concatenated_fields * repeat, output_field=models.CharField())


class ItemQuerySet(models.QuerySet):
    def annotate_search(self) -> "ItemQuerySet":
        return self.annotate(
            search=concat_fields("code", "name", repeat=4),
        )

    def search(self, query: str) -> "ItemQuerySet":
        return self.filter(get_keywords_query(query))


class ItemManager(models.Manager):
    def get_queryset(self) -> ItemQuerySet:
        return ItemQuerySet(self.model, using=self._db)

    def annotate_search(self) -> ItemQuerySet:
        return self.get_queryset().annotate_search()

    def search(self, query: str) -> ItemQuerySet:
        return self.get_queryset().search(query)


class Item(models.Model):
    class IsTouched(models.TextChoices):
        TOUCHED = "touched", _("Touched")
        NOT_TOUCHED = "not_touched", _("Not touched")

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
    serial = models.IntegerField(
        default=0,
        verbose_name=_("Serial"),
    )
    code = models.CharField(
        max_length=255,
        verbose_name=_("Code"),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    initial_qty = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Initial quantity"),
    )
    qty = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Quantity"),
    )
    notes = models.TextField(
        default="",
        blank=True,
        verbose_name=_("Notes"),
    )
    is_touched = models.CharField(
        max_length=20,
        choices=IsTouched.choices,
        default=IsTouched.NOT_TOUCHED,
        verbose_name=_("Is touched"),
    )

    objects: ItemManager = ItemManager()

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        ordering = (
            "serial",
            "name",
            "code",
        )

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"
