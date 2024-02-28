
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
        
        if request.user and request.user.is_staff:
            return True
        return False
    

class IsAdminUSerOrAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        return False  
    
    def has_object_permission(self, request, view, obj):

        if request.user.is_staff or obj.customer == request.user:
            return True
        return False