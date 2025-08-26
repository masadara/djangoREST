import stripe
from django.conf import settings
from typing import Dict, Any

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name: str, description: str = "") -> Dict[str, Any]:
    product = stripe.Product.create(
        name=name,
        description=description,
    )
    return product

def create_stripe_price(product_id: str, unit_amount: int, currency: str = "usd") -> Dict[str, Any]:
    price = stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency=currency,
    )
    return price

def create_stripe_checkout_session(price_id: str, success_url: str, cancel_url: str) -> Dict[str, Any]:
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session
