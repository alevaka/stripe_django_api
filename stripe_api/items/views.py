import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Item

stripe_api_key = 'sk_test_51M6JL2DmksvhmrdClPVTd3k1HFt7IBGDwE9fMaYrfMzZzC50vO7AiysALPjaZ2Ad2NDtr9TDLi6xZwfHQ4G7hk7K00382JZNYF'


def buy_item(request, pk) -> JsonResponse:
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
          # currency='USD',
          line_items=line_items,
          success_url='http://localhost:8000/',
          cancel_url=f'http://localhost:8000/item/{pk}/'
      )

    json_data = {
      'pk': pk,
      'session_id': session.id
    }
    return JsonResponse(json_data)


def show_item(request, pk):
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
