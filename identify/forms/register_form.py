from django import forms

class RegisterOnSite(forms.Form):
    email = forms.EmailField(required=True, help_text='ایمیل کاربر')
    password = forms.CharField(required=True, max_length=20, help_text='پسورد')
    password_2 = forms.CharField(required=True, max_length=20, help_text='تکرار پسور')
    
    def clean_password_2(self):
        password = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_2')

        if password and password_2 and password != password_2:
            raise forms.ValidationError('رمز عبور و تکرار آن یکسان نیستند')

        return password_2
    
    
        
        
    