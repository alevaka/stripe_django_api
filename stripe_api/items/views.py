import os

import stripe
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Item

stripe_api_key = os.getenv('STRIPE_API_PUBLIC_KEY')


def buy_item(request: HttpRequest, pk: int) -> JsonResponse:
    """Функция для покупки одного товара.
    Создаёт Stripe Session и возвращает id сессии"""

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
