from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Formation
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_formations = cart.get_forms()
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_formations": cart_formations, "totals": totals})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        formation_id = int(request.POST.get('formation_id'))
        formation = get_object_or_404(Formation, id=formation_id)
        cart.add(formation=formation)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, "Formation Added to Cart...")
        return response




def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        formation_id = int(request.POST.get('formation_id'))
        cart.delete(formation_id=formation_id)
        response = JsonResponse({'formation': formation_id})
        messages.success(request, "Formation Deleted from Cart...")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        formation_id = int(request.POST.get('formation_id'))
        new_price = float(request.POST.get('new_price'))  # Suppose you are updating the price
        cart.update(formation_id=formation_id, new_price=new_price)
        response = JsonResponse({'form': formation_id})
        return response