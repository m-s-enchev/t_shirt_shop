from django import forms

from t_shirt_shop.contact_form_messages.models import MessagesModel


class MessagesForm(forms.ModelForm):
    class Meta:
        model = MessagesModel
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your names'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your message'}),
        }
