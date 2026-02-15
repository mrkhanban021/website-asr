from django import forms
from website.models import ProductComment


class ProductCommentForms(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['full_name', 'text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  
        self.product = kwargs.pop('product', None) 
        super().__init__(*args, **kwargs)
        if self.user:  # اگر کاربر لاگین است، full_name را مخفی کنیم
            self.fields['full_name'].widget = forms.HiddenInput()
            self.fields['full_name'].required = False

    def save(self, commit=True):
        comment = super().save(commit=False)
        # اگر کاربر لاگین دارد
        if self.user:
            comment.user = self.user
        if self.product:
            comment.product = self.product
        if commit:
            comment.save()
        return comment
    

class ProductCommentReplyForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['full_name', 'text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.parent = kwargs.pop('parent', None)  # کامنت والد
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['full_name'].widget = forms.HiddenInput()
            self.fields['full_name'].required = False

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.user:
            comment.user = self.user
        if self.product:
            comment.product = self.product
        if self.parent:
            comment.parent = self.parent
        if commit:
            comment.save()
        return comment