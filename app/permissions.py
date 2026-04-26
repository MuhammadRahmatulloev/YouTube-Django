from django.shortcuts import redirect
from django.contrib import messages


class SessionLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Please login first!')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class OwnerOrAdminRequiredMixin:
    owner_field  = 'owner'
    fail_redirect = 'home'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'Please login first!')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user_id = self.request.session.get('user_id')

        fields = self.owner_field.split('__')
        owner  = obj
        for field in fields:
            owner = getattr(owner, field)

        if owner.id != user_id:
            from .models import UserModel
            user = UserModel.objects.filter(id=user_id).first()
            if not user or not user.is_admin:
                messages.error(self.request, 'You do not have permission to do this!')
                return redirect(self.fail_redirect)
        return obj