from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterForm, UserLoginForm, CustomerProfileEditForm
from .models import Register, Customer
from django.contrib.auth.views import LoginView

class RegisterView(generic.CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        self.role = self.kwargs.get('role')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.role
        return context
    
    def form_valid(self, form):
        role = 'customer' 
        Register.objects.create_user(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
            user_role = role
        )
        return redirect('user_login')
    
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.user_role != 'customer':
            return self.form_invalid(form)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('homepage')
    
class ProfileView(generic.TemplateView):
    template_name = 'account/profile.html'
    
class CustomerProfileEditView(generic.UpdateView):
    model = Customer
    form_class = CustomerProfileEditForm
    template_name = 'account/customer_profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_object(self):
        return self.request.user.customer_profile