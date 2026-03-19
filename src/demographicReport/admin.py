from django.contrib import admin
from django.contrib.auth.models import User
from .models import UnderrepresentedGroup

@admin.register(UnderrepresentedGroup)
class UnderrepresentedGroupsNameAdmin(admin.ModelAdmin):
    list_display = ("name",)
    def get_queryset(self, request):
        """Filter queryset to show only products created by users in the same user groups as the current user"""
        qs = super().get_queryset(request)
        if request.user.is_superuser: #superuser is exempted
            return qs
        
        # Get all groups the current user belongs to
        user_groups = request.user.groups.all()
        user_group_ids = set(user_groups.values_list('id', flat=True))
    
        # Get all users with the exact same groups
        matching_users = []
        for user in User.objects.prefetch_related('groups'):
            if set(user.groups.values_list('id', flat=True)) == user_group_ids:
                matching_users.append(user.id)
    
        return qs.filter(created_by__id__in=matching_users)

    def save_model(self, request, obj, form, change):
        """Automatically set created_by when creating a new product"""
        if not change:  # Only set created_by when creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_change_permission(self, request, obj=None):
        """Only allow editing if same user groups created the product"""
        if obj is None:
            return True
        if request.user.is_superuser: 
            return True
        
        ##Only allow editing when both users belong to the same groups (LLManager + LLgroup) 
        current_user_groups = set(request.user.groups.values_list('id', flat=True))
        creator_groups = set(obj.created_by.groups.values_list('id', flat=True))

        return current_user_groups == creator_groups 
    
    def has_delete_permission(self, request, obj=None):
        """Only allow deletion if same user groups created the product"""
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        
        ##Only allow deleting when both users belong to the same groups (LLManager + LLgroup) 
        current_user_groups = set(request.user.groups.values_list('id', flat=True))
        creator_groups = set(obj.created_by.groups.values_list('id', flat=True))

        return current_user_groups == creator_groups 
    
    def get_exclude(self, request, obj=None):
        """Hide created_by field from the form"""
        if request.user.is_superuser:
            return []
        return ['created_by']
