from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class RegisterOnSite(forms.Form):
    email = forms.EmailField(required=True, help_text='ایمیل کاربر', error_messages={'required':'ایمیل اجباری'})
    password = forms.CharField(required=True, max_length=20, help_text='پسورد', error_messages={'required':'رمز عبور'})
    password_2 = forms.CharField(required=True, max_length=20, help_text='تکرار پسور', error_messages={
        'required': 'تکرار رمز عبور',
    })
    
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل قبلا ثبت شده است')
        return email
    
    def clean_password_2(self):
        password = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_2')

        if password and password_2 and password != password_2:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند')

        return password_2
    

class LoginOnSite(forms.Form):
    email = forms.EmailField(required=True, help_text='ایمیل کاربر')
    password = forms.CharField(required=True, help_text='رمز عبور')
    
    def clean(self):
        cleaned_data = super().clean()
         
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if not email or not password:
            return cleaned_data
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise forms.ValidationError(
                'ایمیل یا رمز عبور اشتباه است'
            )
            
        self.user = user
         
        return cleaned_data

         
    

    
    
        
        
    