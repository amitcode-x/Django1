from django import forms



class UserForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(max_length=15, label='Phone')
    message = forms.CharField(widget=forms.Textarea, label='Message')