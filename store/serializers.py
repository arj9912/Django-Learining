from collections import OrderedDict
from rest_framework import serializers
from store.models import Collection, OrderItem,Product,Cart, CartItem ,Order

    
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     featured_product= serializers.StringRelatedField()

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=8, decimal_places=2,)
#     inventory = serializers.IntegerField()
#     description = serializers.CharField()
#     collection = CollectionSerializer()


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "featured_product"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name","unit_price", "inventory", "description", "collection"]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name","unit_price"]




class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields =["id","quantity", "product","total_price"]

    def get_total_price(self,cart_item) :
        return cart_item.quantity * cart_item.product.unit_price     



class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ["product_id","quantity"]  

    def create(self, validated_data):
        product_id= validated_data['product_id']
        product=Product.objects.get(id=product_id)
        quantity =validated_data['quantity']
        cart_id= self.context['cart_id']
        ramesh= Cart.objects.get(id=cart_id)
        try:
            
            cart_item=CartItem.objects.get(cart=ramesh,product=product)
            cart_item.quantity=cart_item.quantity + quantity
            cart_item.save()
        except CartItem.DoesNotExist:

            cart_item=CartItem.objects.create(cart=ramesh,product=product,quantity=quantity)
        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]  


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price= serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ["id","total_price", "items"]


    def  get_total_price(self,cart):
        return  sum([item.product.unit_price * item.quantity for item in cart.items.all()])
    
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["id","product","quantity"]


class OrderSerializer(serializers.ModelSerializer):
   
    items=OrderItemSerializer(many=True, source='order_items',read_only=True)
    status=serializers.ReadOnlyField()
    cart_id=serializers.CharField(write_only=True)

    class Meta:
        model = Order
        fields =["id","status","items","cart_id"]

    def create(self, validated_data):
        cart_id= validated_data["cart_id"]
        cart=Cart.objects.get(id=cart_id)
        cart_items=cart.items.all()
        user=self.context["user"]
        order= Order.objects.create(customer=user)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        cart.delete()

        return order
    
            


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]



      



        





        
    



