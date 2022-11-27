from django.db import models


class Item(models.Model):
    """Класс для товара"""

    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    price = models.IntegerField(
        verbose_name='Цена'
    )
    currency = models.CharField(
        max_length=5,
        null=False,
        verbose_name='Валюта'
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    """Класс для корзины (заказа)"""

    item = models.ManyToManyField(
        Item,
        verbose_name='Заказ'
    )

    tax = models.ForeignKey(
        'Tax',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order'
    )

    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        null=True,
        related_name='order'
    )


class Discount(models.Model):
    """Класс для скидки"""

    rate = models.IntegerField(
        verbose_name='Скидка'
    )


class Tax(models.Model):
    """Класс для налога"""

    rate = models.IntegerField(
        verbose_name='Налог'
    )
