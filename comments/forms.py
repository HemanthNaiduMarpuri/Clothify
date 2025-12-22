from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=True, label='Comment')
    reaction = forms.ChoiceField(choices=(('like', 'Like'),('dislike','Dislike')), required=False)