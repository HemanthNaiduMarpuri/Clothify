from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return self.handle_no_permission()
        
        if not user.is_staff or user.user_role != 'admin':
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs) 
    
