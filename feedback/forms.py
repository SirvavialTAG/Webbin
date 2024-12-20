from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'phone_number', 'content', 'privacy_policy_agreed']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите имя',
                'pattern': '^[A-Za-zА-Яа-яЁё\s]+$',
                'title': 'Имя должно содержать только буквы и пробелы.',
                'maxlength': '20',
                'required': True,
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+7',
                'pattern': r'^\+7 [0-6,9]\d{2} \d{3} \d{2} \d{2}$',
                'title': "Формат: '+7 999 999 99 99'",
                'maxlength': '16',
                'required': True,
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Введите текст сообщения, укажите страну, марку и год машины.',
                'maxlength': '200',
                'rows': 10,
                'cols': 40,
            }),
            'privacy_policy_agreed': forms.CheckboxInput(attrs={
                'required': True,
            }),
        }


