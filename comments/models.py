from django.db import models
from accounts.models import Customer
from products.models import Product

class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='commented_on')
    comment = models.TextField()
    likes = models.ManyToManyField(Customer, related_name='reactions_like', blank=True)
    dislikes = models.ManyToManyField(Customer, related_name='reactions_dislike', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.reactions.filter(reaction='like').count()

    def dislike_count(self):
        return self.reactions.filter(reaction='dislike').count()

    def __str__(self):
        return f"{self.customer} -> {self.product}"

class CommentLike(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'comment')