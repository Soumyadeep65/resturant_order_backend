from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('cart/add/', CartViewSet.as_view({'post': 'add'})),
    path('cart/update_quantity/', CartViewSet.as_view({'patch': 'update_quantity'})),
    path('cart/calculate_total/', CartViewSet.as_view({'post': 'calculate_total'}), name='calculate_total'),
    path('orders/place_order/', OrderViewSet.as_view({'post': 'place_order'})),
]
