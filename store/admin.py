from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from store.models import CartItem, Collection, Order, Product ,ProductImage,Cart,OrderItem
# Register your models here.

class ProductImageInlineAdmin(admin.TabularInline):
    model = ProductImage
    extra = 2
    max_num =5
    min_num = 1    
    list_display=('id','product', 'image')






class StatusFilter(admin.SimpleListFilter):
    title ="Status"
    parameter_name = "Status"

    def lookups(self, request, model_admin):
        return {
            ("low" ,"Low"),
            ("high" ,"High")
            
        }




    

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(inventory__lt=10)
        
        if self.value() == "high":

            return queryset.filter(inventory__gt=19)






@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions =('clear_inventory_action',)
    list_display=('name', 'unit_price', 'inventory','status')
    list_filter=(StatusFilter ,)
    search_fields=('name','collection__name')
    inlines = (ProductImageInlineAdmin,)


    @admin.display(ordering='inventory')
    def status(self,product):
        if product.inventory < 10:
            return 'Low'
        
        elif product.inventory>=10 and product.inventory<20:
            return 'Ok'
        
        return 'High'
    

    @admin.action(description='Clear Inventory')
    def clear_inventory_action(self,request,queryset):
        queryset.update(inventory=0)
        self.message_user(request,"Successfully cleared Inventory")

            





@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=('id','name','featured_product')    




# admin.site.register(Collection)
class CartItemInlineAdmin(admin.TabularInline):
    model = CartItem
    extra =2
    max_num=3
    min_num =1
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=("id","modified_at","created_at")
    inlines= (CartItemInlineAdmin,)

    

class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    extra= 2
    max_num=3
    min_num=1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=("id",)
    inlines=(OrderItemInlineAdmin,)
    
