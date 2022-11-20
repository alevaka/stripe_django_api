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

    def __str__(self):
        return self.name


class Order(models.Model):
    """Класс для корзины (заказа)"""

    item = models.ManyToManyField(
        Item,
        through='OrderItem',
        verbose_name='Заказ'
    )

    def __str__(self):
        pass


class Discount(models.Model):
    """Класс для скидки"""

    rate = models.IntegerField(
        verbose_name='Скидка'
    )

    pass


class Tax(models.Model):
    """Класс для налога"""

    rate = models.IntegerField(
        verbose_name='Налог'
    )

    pass
