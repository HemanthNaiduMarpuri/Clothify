from django.shortcuts import redirect, render
from .models import Comment, CommentLike
from .forms import CommentForm
from django.views import View, generic
from accounts.models import Customer
from products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class CommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        customer = get_object_or_404(Customer, user=request.user)
        product = get_object_or_404(Product, pk=pk)
        slug = product.product_slug
        
        form = CommentForm(request.POST)
        if not form.is_valid():
            return redirect(request.META.get('HTTP_REFERER', '/'))
        comment_text = form.cleaned_data['comment']
        reaction = form.cleaned_data['reaction']

        comment_obj, created = Comment.objects.update_or_create(
            customer=customer,
            product=product,
            defaults={'comment':comment_text}
        )

        if reaction:
            reaction_obj, created = CommentLike.objects.get_or_create(
                comment=comment_obj,
                customer=customer,
                defaults={'reaction':reaction}
            )

            if not created:
                if reaction_obj.reaction == reaction:
                    reaction_obj.delete()
                else:
                    reaction_obj.reaction = reaction
                    reaction_obj.save()
        return redirect('product_detail', product_slug=slug)
    
@login_required(login_url='account_login')
def comment_like(request, id):
    comment = get_object_or_404(Comment, id=id)
    if not request.user.is_authenticated:
        return redirect('account_login')
    customer = Customer.objects.get(user=request.user)
    slug = comment.product.product_slug

    if customer in comment.likes.all():
        comment.likes.remove(customer)
    else:
        comment.likes.add(customer)
        comment.dislikes.remove(customer)

    return redirect('product_detail', product_slug=slug)


@login_required(login_url='account_login')
def comment_dislike(request, id):
    comment = get_object_or_404(Comment, id=id)
    if not request.user.is_authenticated:
        return redirect('account_login')
    customer = Customer.objects.get(user=request.user)
    slug = comment.product.product_slug

    if customer in comment.likes.all():
        comment.dislikes.remove(customer)
    else:
        comment.dislikes.add(customer)
        comment.likes.remove(customer)

    return redirect('product_detail', product_slug=slug)

@require_POST
@login_required(login_url='account_login')
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    slug = comment.product.product_slug
    if not request.user.is_authenticated:
        return redirect('account_login')
    customer = Customer.objects.get(user=request.user)

    if comment.customer == customer:
        comment.delete()
    return redirect('product_detail', product_slug=slug)

