from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

class OwnsVideo(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj.author.id == request.user.id