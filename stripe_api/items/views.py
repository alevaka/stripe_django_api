import os
import json

import stripe
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Item, Order

stripe_api_key = os.getenv('STRIPE_API_PUBLIC_KEY')


def buy_item(request: HttpRequest, pk: int) -> JsonResponse:
    """Функция для покупки одного товара.
       Создаёт Stripe Session и возвращает id сессии."""

    line_items = []
    item = get_object_or_404(Item, pk=pk)
    line_items.append(
        {
          'price_data': {
            'currency': item.currency,
            'product_data': {
              'name': item.name,
            },
            'unit_amount': item.price * 100
          },
          'quantity': 1,
        },
    )
    session = stripe.checkout.Session.create(
          api_key=stripe_api_key,
          mode='payment',
          line_items=line_items,
          success_url=f'http://localhost:8000/item/{pk}/',
          cancel_url=f'http://localhost:8000/item/{pk}/'
      )

    json_data = {
      'pk': pk,
      'session_id': session.id
    }
    return JsonResponse(json_data)


def show_item(request: HttpRequest, pk: int) -> HttpResponse:
    """Функция для показа страницы товара."""

    template = 'items/item.html'
    item = get_object_or_404(Item, pk=pk)
    currency_symbols = {
      'USD': '$',
      'RUB': '₽'
    }
    context = {
      'pk': pk,
      'name': item.name,
      'description': item.description,
      'price': item.price,
      'currency': currency_symbols[item.currency]
    }

    return render(request, template, context)


def create_order(request: HttpRequest) -> JsonResponse:
    """Создает новый заказ и возвращает его id."""

    order = Order.objects.create()
    return JsonResponse({'order_id': order.id})


def add_item_to_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Добавляет товар в заказ.
       Номер заказа необходимо передать в теле запроса."""

    order_id = json.loads(request.body)['order_id']
    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(Item, pk=pk)
    order.item.add(item)
    items = []
    for item in order.item.all():
        items.append(str(item))
    return JsonResponse({'order_items': items})


def exchange_rate(currency_from: str, currency_to: str) -> int:
    """Конвертация валют.
       Для тестирования примем, что у нас только две валюты
       и курс у них стабилен."""
    rates = {
        'USD_RUB': 60,
        'RUB_USD': 0.0166667,
    }
    return rates.get(f'{currency_from}_{currency_to}') or 9999


def pay_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Оплата заказа. Цена всех товаров конвертируется в валюту первого товара.
    Создаёт Stripe Session и возвращает id сессии"""

    order = get_object_or_404(Order, pk=pk)
    line_items = []
    first_currency = None
    for item in order.item.all():
        first_currency = first_currency or item.currency
        converted_price = (item.price if first_currency == item.currency
                           else exchange_rate(item.currency, first_currency)
                           * item.price)
        line_items.append(
            {
              'price_data': {
                'currency': first_currency,
                'product_data': {
                  'name': item.name,
                },
                'unit_amount': int(converted_price * 100)
              },
              'quantity': 1,
            },
        )

    session = stripe.checkout.Session.create(
          api_key=stripe_api_key,
          mode='payment',
          line_items=line_items,
          success_url=f'http://localhost:8000/order/{pk}/',
          cancel_url=f'http://localhost:8000/order/{pk}/'
      )

    json_data = {
      'pk': pk,
      'session_id': session.id
    }
    return JsonResponse(json_data)


def show_order(request: HttpRequest, pk: int) -> JsonResponse:
    """Возвращает JSON списка товаров в заказе"""

    order = get_object_or_404(Order, pk=pk)
    items = []
    for item in order.item.all():
        items.append(str(item))
    return JsonResponse({'order_items': items})
