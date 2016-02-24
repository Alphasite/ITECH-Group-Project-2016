from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))