
from django.urls import path
from. import views

# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='products')
router.register('carts', views.CartViewSet, basename='carts')
router.register('orders', views.OrderViewSet, basename='orders')

cart_router =  NestedDefaultRouter(router, 'carts', lookup='cart')

cart_router.register('items', views.CartItemViewSet, basename='cart-items')



urlpatterns = [

    # path('home/',views.home),
    # path('hello/',views.hello),
    # path('products-list/',views.products_list),
    # path('product-detail/<int:id>/',views.product_detail),
    # path('collections-list/',views.collections_list),
    # path('collection-detail/<int:id>/',views.collection_detail),

    # path('product-list/',views.ProductList.as_view()),

    
]


urlpatterns = urlpatterns + router.urls + cart_router.urls
