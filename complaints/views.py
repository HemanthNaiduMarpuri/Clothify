from django.shortcuts import redirect, render
from django.views import generic
from .models import Complaints
from django.contrib.auth.decorators import login_required
from accounts.models import Customer
from django.contrib import messages

class ComplaintsListView(generic.ListView):
    model = Complaints
    template_name = 'complaints/complaints_list.html'
    context_object_name = 'complaints'
    ordering = ['-created_at']

@login_required
def complaint(request):
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        fullname = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not fullname or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('contact')
        
        Complaints.objects.create(
            customer=customer,
            full_name = fullname,
            email=email,
            complaint_msg=message
        )

        messages.success(request, "Your complaint has been submitted successfully.")
        return redirect('contact')

    return render(request, 'contactus.html')
    