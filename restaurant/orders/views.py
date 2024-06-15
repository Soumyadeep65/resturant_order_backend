from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Cart, CartItem, Order,Option
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer
from .serializers import OptionListSerializer
from decimal import Decimal

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['get'])
    def options(self, request, pk=None):
        product = self.get_object()
        option_lists = product.option_lists.all()
        serializer = OptionListSerializer(option_lists, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=['post'])
    def add(self, request):
        cart, created = Cart.objects.get_or_create(id=request.data.get('cart_id'))
        product = Product.objects.get(id=request.data.get('product_id'))
        quantity = request.data.get('quantity', 1)
        options = request.data.get('options', [])
        
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        # Extracting option IDs from the full option list
        option_ids = [option['id'] for option in options]
        option_objects = Option.objects.filter(id__in=option_ids)
        cart_item.options.set(option_objects)
        cart_item.save()
        
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        try:
            cart_item = CartItem.objects.get(id=request.data.get('cart_item_id'))
            quantity = request.data.get('quantity')
            cart_item.quantity = quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data)
        except CartItem.DoesNotExist:
            return Response({'error': 'CartItem not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def calculate_total(self, request):
        try:
            cart_id = request.data.get('cart_id')
            cart = Cart.objects.get(id=cart_id)
            
            total_price = Decimal('0.0')
            for item in cart.items.all():
                item_total = item.product.base_price * item.quantity
                options_total = sum(Decimal(opt.surcharge) for opt in item.options.all())
                total_price += item_total + options_total
            
            tax = total_price * Decimal('0.1')
            service_fee = total_price * Decimal('0.05')
            tip = Decimal(request.data.get('tip', '0.0'))

            total_price += tax + service_fee + tip
            
            return Response({
                'total_price': total_price,
                'tax': tax,
                'service_fee': service_fee,
                'tip': tip
            })
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_cart_by_id(self, request):
        try:
            cart_id = request.query_params.get('cart_id')
            cart = Cart.objects.get(id=cart_id)
            return Response(CartSerializer(cart).data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def place_order(self, request):
        try:
            cart = Cart.objects.get(id=request.data.get('cart_id'))
            total_price = request.data.get('total_price')
            tax = request.data.get('tax')
            service_fee = request.data.get('service_fee')
            tip = request.data.get('tip')

            order = Order.objects.create(
                cart=cart,
                total_price=total_price,
                tax=tax,
                service_fee=service_fee,
                tip=tip
            )

            return Response(OrderSerializer(order).data)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
