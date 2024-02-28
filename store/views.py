from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Q , F , ExpressionWrapper ,FloatField
from rest_framework.decorators import api_view
from store.models import Collection, Product ,Cart, CartItem,Order
from store.serializers import CollectionSerializer, OrderSerializer, ProductSerializer, CartSerializer , CartItemSerializer, CreateCartItemSerializer, UpdateCartItemSerializer, UpdateOrderSerializer
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from store.filters import ProductFilter
from store.pagination import CustomPagination
from store.permissons import IsAdminUSerOrAuthenticatedReadOnly, IsAdminUserOrReadOnly

# Create your views here.

def home(request):
    
    discount_price= ExpressionWrapper(F('unit_price') * 0.9,output_field=FloatField())
    # products= Product.objects.filter( Q(name__icontains="ice cream") | Q(unit_price__gt=200))
    products= Product.objects.select_related('collection').annotate(discount_price=discount_price).order_by('-inventory')
    #     product= Product.objects.get(name="Mushroom - Chvbrimini")
    # except Product.DoesNotExist:
    #     product=None

    total_products= Product.objects.count()


    return render(request,'home.html',{"total_products":total_products,"products":list(products)})
    # return render(request,'home.html',{"product":product})



@api_view()
def hello(request):
    return Response({"message":"Hello World"})



# class ProductList(APIView):
#     def get(self,request):
#         products = Product.objects.all()[:10]
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data)
            
#     def post(self,request):
#         data = request.data
#         serializer = ProductSerializer(data=data)
#         try:
#             serializer.is_valid()
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'POST',])
# def products_list(request):
#     products = Product.objects.select_related('collection').all()[:10]
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name","description","collection__name"]
    ordering_fields = ["unit_price","inventory"]
    pagination_class = CustomPagination
    permission_classes = [IsAdminUserOrReadOnly]

    # def get_queryset(self):
    #     ram = self.request.query_params.get("collection_id")
    #     if ram is not None:
    #         qs = Product.objects.filter(collection_id=ram)
    #     else:
    #         qs = Product.objects.all()
    #     return qs
        




class CartViewSet(ModelViewSet):
    http_method_names= ['get', 'post', 'delete']
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch','delete']

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    
class OrderViewSet(ModelViewSet):
    http_method_names=["get","post","patch","option","head","delete"]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == "list":
            return [IsAdminUser()]
        return [IsAdminUSerOrAuthenticatedReadOnly()]


    def get_serializer_class(self):
        if self.request.method=='PATCH':
            return UpdateOrderSerializer
        return OrderSerializer


    def get_serializer_context(self):
        return {'user':self.request.user}
    