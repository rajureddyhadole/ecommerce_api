from cart.models import CartItem
from django.db import transaction
from .models import Order, OrderItem

class EmptyCartError(Exception):
  pass

class OutOfStock(Exception):
  pass

def place_order(user, shipping_address):
  cart_items = CartItem.objects.filter(cart__user=user).select_related("product")

  if not cart_items.exists():
    raise EmptyCartError("The cart is empty.")
  
  total = 0
  for item in cart_items:
    available_stock = item.product.stock_quantity

    if available_stock < item.quantity:
      raise OutOfStock(f"Out of stock.{item.product.name} Only {available_stock} items are available.")
    
    total += item.sub_total

  with transaction.atomic():
  
    order = Order.objects.create(
      user=user,
      total_amount=total,
      shipping_address=shipping_address,
      payment_status='pending'
    )

    for item in cart_items:

      OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity,
        bought_price=item.product.price,
        status='pending'
      )

      item.product.stock_quantity -= item.quantity

      item.product.save()
    
    cart_items.delete()

  return order




###################################
class PayFailed(Exception):
  pass

class PayAlreadyDone(Exception):
  pass

def pay_order(order, result):

  if order.payment_status == order.PaymentStatus.PENDING:
  
    if result == "success":
      order.payment_status = order.PaymentStatus.PAID
      order.save()
    elif result == "failure":
      raise PayFailed("Payment failed!!")
    
  else:
    raise PayAlreadyDone("payment is already done!!")

  return order
    
  

